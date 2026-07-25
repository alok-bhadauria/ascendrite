import os
import sys
import json
import argparse
from pymongo import MongoClient

# Add platform/server directory to PYTHONPATH
script_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.join(os.path.dirname(script_dir), "platform", "server")
if server_dir not in sys.path:
    sys.path.append(server_dir)

from app.core.config import settings

def parse_args():
    parser = argparse.ArgumentParser(description="Ascendrite Knowledge Ingestion & Seeding Engine")
    parser.add_argument(
        "--config",
        type=str,
        default=os.path.join(os.path.dirname(script_dir), "config", "local-seeds.json"),
        help="Path to JSON seeds configuration profile"
    )
    return parser.parse_args()

def load_seed_config(config_path):
    if not os.path.exists(config_path):
        print(f"Seed configuration file not found at: '{config_path}'")
        # Return default fallback parameters
        return {
            "kb_path": "platform/server/app/knowledge-base",
            "categories": ["ai", "core-cs", "software-engineering", "web-development"]
        }
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load seed configuration profile: {e}")
        return None

def seed_catalog(config):
    repo_root = os.path.dirname(script_dir)
    kb_path = os.path.join(repo_root, config.get("kb_path", "platform/server/app/knowledge-base"))
    categories = config.get("categories", [])
    
    print(f"Ingesting knowledge base assets from: '{kb_path}'")
    if not os.path.exists(kb_path):
        print(f"Error: Knowledge base directory '{kb_path}' does not exist.")
        return False
        
    try:
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DB_NAME]
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return False

    for cat in categories:
        cat_path = os.path.join(kb_path, cat)
        if not os.path.exists(cat_path):
            continue
            
        for sub in os.listdir(cat_path):
            sub_path = os.path.join(cat_path, sub)
            if not os.path.isdir(sub_path):
                continue
                
            syllabus_file = os.path.join(sub_path, "syllabus.json")
            metadata_file = os.path.join(sub_path, "subject-metadata.json")
            
            if os.path.exists(syllabus_file) and os.path.exists(metadata_file):
                print(f"Ingesting subject catalog tracks at: '{sub_path}'...")
                try:
                    with open(metadata_file, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    with open(syllabus_file, "r", encoding="utf-8") as f:
                        syllabus = json.load(f)
                        
                    subject_id = sub
                    
                    # 1. Ingest Subject doc
                    db["subjects"].replace_one(
                        {"subject_id": subject_id},
                        {
                            "subject_id": subject_id,
                            "category": cat,
                            "name": meta.get("name", subject_id.replace("-", " ").title()),
                            "difficulty": meta.get("difficulty", "Medium"),
                            "estimated_hours": meta.get("estimated_hours", 40),
                            "is_active": True
                        },
                        upsert=True
                    )
                    
                    # 2. Ingest Syllabus / Modules & Topics
                    db["syllabuses"].replace_one(
                        {"subject_id": subject_id},
                        {
                            "subject_id": subject_id,
                            "name": meta.get("name", subject_id.replace("-", " ").title()) + " Syllabus",
                            "version": "1.0",
                            "modules": syllabus.get("modules", [])
                        },
                        upsert=True
                    )
                    
                    # Parse modules and topics mapping docs
                    for m in syllabus.get("modules", []):
                        module_id = m.get("id")
                        db["modules"].replace_one(
                            {"id": module_id},
                            {
                                "id": module_id,
                                "subject_id": subject_id,
                                "name": m.get("title"),
                                "order": 1,
                                "description": m.get("description", "")
                            },
                            upsert=True
                        )
                        
                        # Ingest individual topics
                        for idx, topic_name in enumerate(m.get("topics", [])):
                            # Convert topic name to slug format
                            topic_id = f"{module_id}-t{idx+1}"
                            db["topics"].replace_one(
                                {"topic_id": topic_id},
                                {
                                    "topic_id": topic_id,
                                    "module_id": module_id,
                                    "subject_id": subject_id,
                                    "name": topic_name,
                                    "order": idx + 1,
                                    "description": f"Master principles for {topic_name}"
                                },
                                upsert=True
                            )
                            
                    # 3. Check for topic notes text contents under notes/ directory
                    notes_path = os.path.join(sub_path, "notes")
                    if os.path.exists(notes_path):
                        for note_file in os.listdir(notes_path):
                            if not note_file.endswith(".json"):
                                continue
                            note_file_path = os.path.join(notes_path, note_file)
                            topic_id = note_file.replace(".json", "")
                            
                            try:
                                with open(note_file_path, "r", encoding="utf-8") as f:
                                    note_data = json.load(f)
                                    
                                # Ingest as knowledge contents
                                db["knowledge_contents"].replace_one(
                                    {"topic_id": topic_id},
                                    {
                                        "topic_id": topic_id,
                                        "subject_id": subject_id,
                                        "title": note_data.get("title", topic_id),
                                        "body": note_data.get("content", ""),
                                        "attachments": note_data.get("attachments", []),
                                        "publication_state": "Published"
                                    },
                                    upsert=True
                                )
                                print(f"  Mapped topic notes content file: '{note_file}'")
                            except Exception as ex:
                                print(f"  Failed to parse notes content '{note_file_path}': {ex}")
                                
                except Exception as e:
                    print(f"Failed to ingest subject track '{sub}': {e}")
                    
    print("Catalog indexing seeder finished mapping records to MongoDB.")
    return True

def main():
    print("======================================================================")
    print("               ASCENDRITE KNOWLEDGE CATALOG MIGRATION SEEDER          ")
    print("======================================================================")
    args = parse_args()
    config = load_seed_config(args.config)
    if config:
        seed_catalog(config)
    else:
        print("Knowledge base migration failed.")

if __name__ == "__main__":
    main()

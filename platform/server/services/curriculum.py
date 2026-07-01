import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class CurriculumService:
    def __init__(self):
        self.kb_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            "knowledge-base"
        )
        self.subject_dir_map: Dict[str, str] = {}  # subject_id -> absolute_dir_path
        self.subjects_index: List[Dict[str, Any]] = []
        self.load_curriculum_index()

    def load_curriculum_index(self):
        logger.info(f"Scanning knowledge-base directory structures at: '{self.kb_path}'")
        if not os.path.exists(self.kb_path):
            logger.error(f"Knowledge Base path '{self.kb_path}' not found.")
            return

        categories = ["ai", "core-cs", "software-engineering", "web-development", "aptitude"]
        for cat in categories:
            cat_path = os.path.join(self.kb_path, cat)
            if not os.path.exists(cat_path):
                continue
            for sub in os.listdir(cat_path):
                sub_path = os.path.join(cat_path, sub)
                if not os.path.isdir(sub_path):
                    continue
                
                syllabus_file = os.path.join(sub_path, "syllabus.json")
                metadata_file = os.path.join(sub_path, "subject-metadata.json")
                
                if os.path.exists(syllabus_file) and os.path.exists(metadata_file):
                    try:
                        with open(syllabus_file, "r", encoding="utf-8") as f:
                            syllabus = json.load(f)
                        with open(metadata_file, "r", encoding="utf-8") as f:
                            metadata = json.load(f)
                        
                        subject_id = sub
                        self.subject_dir_map[subject_id] = sub_path
                        
                        subject_data = {
                            "subject_id": subject_id,
                            "category": cat,
                            "name": metadata.get("name", subject_id.replace("-", " ").title()),
                            "metadata": metadata,
                            "modules": syllabus.get("modules", [])
                        }
                        self.subjects_index.append(subject_data)
                    except Exception as e:
                        logger.error(f"Failed to load subject profile at '{sub_path}': {e}")
        
        logger.info(f"Loaded index caches for {len(self.subjects_index)} subjects.")

    def get_subjects_index(self) -> List[Dict[str, Any]]:
        return self.subjects_index

    def get_subject(self, subject_id: str) -> Optional[Dict[str, Any]]:
        for sub in self.subjects_index:
            if sub["subject_id"] == subject_id:
                return sub
        return None

    def get_topic_asset(self, subject_id: str, asset_type: str, topic_id: str) -> Optional[Dict[str, Any]]:
        sub_path = self.subject_dir_map.get(subject_id)
        if not sub_path:
            return None

        # Resolve asset file suffix mappings
        suffix_map = {
            "notes": "",
            "revision": "",
            "interview": "",
            "diagrams": "-dia1",
            "examples": "-ex1",
            "practice": "-prac1",
            "quiz": "-quiz"
        }
        
        if asset_type not in suffix_map:
            return None
            
        suffix = suffix_map[asset_type]
        filename = f"{topic_id}{suffix}.json"
        file_path = os.path.join(sub_path, asset_type, filename)
        
        if not os.path.exists(file_path):
            logger.warning(f"Curriculum asset file not found: '{file_path}'")
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load dynamic asset content from '{file_path}': {e}")
            return None

curriculum_service = CurriculumService()

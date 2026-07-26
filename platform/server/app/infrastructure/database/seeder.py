import os
import json
import logging
import uuid
from datetime import datetime, timezone
from bson import ObjectId
from app.core.config import settings
from app.infrastructure.database.mongodb import db_manager
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)

async def seed_database_from_knowledge_base():
    """Reads curriculum subjects and syllabuses from knowledge-base path and seeds MongoDB collection tables.
    Also seeds test profiles & local identities for student, creator, and admin accounts if empty.
    """
    db = db_manager.db
    if db is None:
        logger.error("Seeder cannot execute: MongoDB connection is empty.")
        return

    # 1. Seed Curriculum Metadata
    count = await db["subjects"].count_documents({})
    if count == 0:
        kb_path = settings.KNOWLEDGE_BASE_PATH or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            "knowledge-base"
        )
        logger.info(f"Database empty. Scanning knowledge-base directory structures at: '{kb_path}' to seed MongoDB...")
        
        if os.path.exists(kb_path):
            categories = ["ai", "core-cs", "software-engineering", "web-development", "aptitude"]
            subjects_seeded = 0
            syllabuses_seeded = 0
            modules_seeded = 0
            topics_seeded = 0

            current_time = datetime.now(timezone.utc)

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
                        try:
                            with open(syllabus_file, "r", encoding="utf-8") as f:
                                syllabus_data = json.load(f)
                            with open(metadata_file, "r", encoding="utf-8") as f:
                                metadata_data = json.load(f)
                            
                            subject_id = sub
                            subject_name = metadata_data.get("name", subject_id.replace("-", " ").title())
                            
                            # Seed Subject
                            subject_doc = {
                                "_id": subject_id,
                                "name": subject_name,
                                "code": metadata_data.get("code", subject_id.replace("-", "").upper()[:6]),
                                "description": metadata_data.get("description", f"Master {subject_name} parameters."),
                                "category": cat,
                                "status": "active",
                                "created_by": "admin",
                                "created_at": current_time,
                                "updated_at": current_time,
                                "metadata": metadata_data
                            }
                            await db["subjects"].insert_one(subject_doc)
                            subjects_seeded += 1
                            
                            # Seed Syllabus
                            syllabus_id = str(uuid.uuid4())
                            syllabus_doc = {
                                "_id": syllabus_id,
                                "subject_id": subject_id,
                                "name": f"{subject_name} Syllabus",
                                "version": "1.0.0",
                                "description": f"Master syllabus outline structure for {subject_name}.",
                                "status": "active",
                                "created_by": "admin",
                                "created_at": current_time,
                                "updated_at": current_time,
                                "metadata": {}
                            }
                            await db["syllabuses"].insert_one(syllabus_doc)
                            syllabuses_seeded += 1
                            
                            # Seed Modules and Topics
                            modules = syllabus_data.get("modules", [])
                            for mod_idx, mod in enumerate(modules, start=1):
                                module_id = str(uuid.uuid4())
                                module_doc = {
                                    "_id": module_id,
                                    "syllabus_id": syllabus_id,
                                    "name": mod.get("name", f"Module {mod_idx}"),
                                    "order": mod_idx,
                                    "description": mod.get("description", f"Module {mod_idx} of {subject_name}."),
                                    "status": "active",
                                    "created_by": "admin",
                                    "created_at": current_time,
                                    "updated_at": current_time,
                                    "metadata": {}
                                }
                                await db["modules"].insert_one(module_doc)
                                modules_seeded += 1
                                
                                topics_list = mod.get("topics", [])
                                for top_idx, top in enumerate(topics_list, start=1):
                                    if isinstance(top, dict):
                                        topic_id = top.get("id") or str(uuid.uuid4())
                                        topic_name = top.get("title") or top.get("name") or f"Topic {top_idx}"
                                        subtopics = top.get("subtopics", [])
                                    else:
                                        topic_id = str(uuid.uuid4())
                                        topic_name = str(top)
                                        subtopics = []
                                        
                                    topic_doc = {
                                        "_id": topic_id,
                                        "module_id": module_id,
                                        "name": topic_name,
                                        "order": top_idx,
                                        "description": " | ".join(subtopics) if subtopics else f"Topic {top_idx} for module {mod.get('name')}.",
                                        "status": "active",
                                        "created_by": "admin",
                                        "created_at": current_time,
                                        "updated_at": current_time,
                                        "metadata": {"subtopics": subtopics}
                                    }
                                    await db["topics"].insert_one(topic_doc)
                                    topics_seeded += 1
                                    
                        except Exception as e:
                            logger.error(f"Failed to seed curriculum subject '{sub}': {e}")
                            
            logger.info(f"Database Seeder Finished: seeded {subjects_seeded} subjects, {syllabuses_seeded} syllabuses, {modules_seeded} modules, {topics_seeded} topics.")
        else:
            logger.error(f"Seeder failed: Knowledge Base path '{kb_path}' not found.")
    else:
        logger.info(f"Database subjects collection is populated (Count: {count}). Skipping curriculum auto-seeding.")

    # 2. Seed Test Users and Local Identities
    user_count = await db["users"].count_documents({})
    if user_count == 0:
        logger.info("Database users collection is empty. Seeding student, creator, and admin test accounts...")
        current_time = datetime.now(timezone.utc)
        pwd_hash = get_password_hash("Password@123")

        test_users = [
            {
                "email": "student@ascendrite.com",
                "first_name": "Test",
                "last_name": "Student",
                "role": "Student",
            },
            {
                "email": "creator@ascendrite.com",
                "first_name": "Test",
                "last_name": "Creator",
                "role": "Contributor",
            },
            {
                "email": "admin@ascendrite.com",
                "first_name": "Test",
                "last_name": "Admin",
                "role": "Admin",
            }
        ]

        for u in test_users:
            try:
                user_id = ObjectId()
                user_doc = {
                    "_id": user_id,
                    "email": u["email"],
                    "first_name": u["first_name"],
                    "last_name": u["last_name"],
                    "role": u["role"],
                    "profile_picture_url": None,
                    "bio": f"I am a {u['role']} user on Ascendrite.",
                    "education": [],
                    "social_links": {"github": None, "linkedin": None, "twitter": None},
                    "skills": [],
                    "preferences": {"theme": "dark", "notifications_enabled": True},
                    "is_active": True,
                    "created_at": current_time,
                    "updated_at": current_time,
                    "is_deleted": False
                }
                await db["users"].insert_one(user_doc)

                identity_doc = {
                    "_id": ObjectId(),
                    "user_id": str(user_id),
                    "provider": "local",
                    "provider_user_id": u["email"],
                    "password_hash": pwd_hash,
                    "mfa_enabled": False,
                    "failed_login_attempts": 0,
                    "locked_until": None,
                    "last_login_at": None,
                    "created_at": current_time,
                    "updated_at": current_time,
                    "is_deleted": False
                }
                await db["identities"].insert_one(identity_doc)
                logger.info(f"Seeded user profile & local identity for: {u['email']} (Role: {u['role']})")
            except Exception as e:
                logger.error(f"Failed to seed user '{u['email']}': {e}")
    else:
        logger.info(f"Database users collection is populated (Count: {user_count}). Skipping user seeding.")

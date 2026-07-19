import logging
from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException
from app.core.runtime.context import RuntimeContext
from app.modules.learning.schemas.discovery import DiscoverableResource

logger = logging.getLogger(__name__)

class DiscoveryService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    def _require_capability(self, context: RuntimeContext, capability: str) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        if context.principal.role == "Admin":
            return
        if capability not in context.principal.capabilities:
            raise ForbiddenException(f"Principal context is missing required capability: '{capability}'.")

    async def search(
        self,
        query: str,
        filters: Dict[str, Any],
        context: RuntimeContext
    ) -> List[DiscoverableResource]:
        self._require_capability(context, "learning:read")

        results: List[DiscoverableResource] = []
        regex_query = {"$regex": query, "$options": "i"} if query else None

        # Build list of collection configurations
        # Format: (collection_name, resource_type, name_field, desc_field, topic_id_field)
        configs = [
            ("subjects", "subject", "name", "description", None),
            ("syllabuses", "syllabus", "name", "description", None),
            ("modules", "module", "name", "description", None),
            ("topics", "topic", "name", "description", None),
            ("knowledge_contents", "content", "title", "body", "topic_id"),
            ("assessments", "assessment", "title", "description", "topic_id")
        ]

        target_types = filters.get("resource_type")
        if target_types:
            if isinstance(target_types, str):
                target_types = [target_types]
            configs = [c for c in configs if c[1] in target_types]

        for col_name, res_type, name_f, desc_f, topic_id_f in configs:
            q: Dict[str, Any] = {}
            if regex_query:
                q["$or"] = [{name_f: regex_query}]
                if desc_f:
                    q["$or"].append({desc_f: regex_query})

            # Apply filters
            if "difficulty" in filters and res_type in ["content", "assessment"]:
                q["metadata.difficulty"] = filters["difficulty"]
            if "topic_id" in filters and topic_id_f:
                q[topic_id_f] = filters["topic_id"]

            try:
                cursor = self.db[col_name].find(q).limit(20)
                docs = await cursor.to_list(length=20)
                for d in docs:
                    title = d.get(name_f) or ""
                    desc = d.get(desc_f) or ""
                    # Truncate long descriptions
                    if len(desc) > 200:
                        desc = desc[:200] + "..."

                    results.append(DiscoverableResource(
                        resource_id=str(d["_id"]),
                        resource_type=res_type,
                        title=title,
                        description=desc,
                        metadata=d.get("metadata") or {}
                    ))
            except Exception as e:
                logger.error(f"Failed to query collection '{col_name}': {e}")

        return results

    async def get_related_resources(
        self,
        resource_id: str,
        resource_type: str,
        context: RuntimeContext
    ) -> List[DiscoverableResource]:
        self._require_capability(context, "learning:read")

        # Dynamically find related resources.
        # e.g., if content or assessment, find others with same topic_id.
        topic_id = None
        if resource_type == "content":
            doc = await self.db["knowledge_contents"].find_one({"_id": resource_id})
            if doc:
                topic_id = doc.get("topic_id")
        elif resource_type == "assessment":
            doc = await self.db["assessments"].find_one({"_id": resource_id})
            if doc:
                topic_id = doc.get("topic_id")

        if not topic_id:
            return []

        # Find contents and assessments matching the topic_id
        results: List[DiscoverableResource] = []
        
        # Related Contents
        contents_cursor = self.db["knowledge_contents"].find({"topic_id": topic_id, "_id": {"$ne": resource_id}}).limit(5)
        contents = await contents_cursor.to_list(length=5)
        for c in contents:
            results.append(DiscoverableResource(
                resource_id=str(c["_id"]),
                resource_type="content",
                title=c.get("title") or "",
                description=c.get("body")[:100] + "..." if c.get("body") else "",
                metadata=c.get("metadata") or {}
            ))

        # Related Assessments
        assessments_cursor = self.db["assessments"].find({"topic_id": topic_id, "_id": {"$ne": resource_id}}).limit(5)
        assessments = await assessments_cursor.to_list(length=5)
        for a in assessments:
            results.append(DiscoverableResource(
                resource_id=str(a["_id"]),
                resource_type="assessment",
                title=a.get("title") or "",
                description=a.get("description") or "",
                metadata=a.get("metadata") or {}
            ))

        return results

    async def explore(self, context: RuntimeContext) -> Dict[str, List[DiscoverableResource]]:
        self._require_capability(context, "learning:read")

        # "Recently Added" resources
        recently_added: List[DiscoverableResource] = []
        configs = [
            ("knowledge_contents", "content", "title", "body"),
            ("assessments", "assessment", "title", "description")
        ]

        for col_name, res_type, name_f, desc_f in configs:
            try:
                cursor = self.db[col_name].find().sort("created_at", -1).limit(5)
                docs = await cursor.to_list(length=5)
                for d in docs:
                    desc = d.get(desc_f) or ""
                    recently_added.append(DiscoverableResource(
                        resource_id=str(d["_id"]),
                        resource_type=res_type,
                        title=d.get(name_f) or "",
                        description=desc[:100] + "..." if len(desc) > 100 else desc,
                        metadata=d.get("metadata") or {}
                    ))
            except Exception as e:
                logger.error(f"Failed to fetch explore stats for '{col_name}': {e}")

        # Return categorized lists
        return {
            "recently_added": recently_added
        }

from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.search.base import SearchDocument, SearchProvider

class MongoSearchProvider(SearchProvider):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["search_index"]

    async def index_document(self, doc: SearchDocument) -> None:
        doc_dict = doc.model_dump(by_alias=True)
        # Use composite primary key identifier check for search document index updates
        await self.collection.replace_one(
            {"_id": doc.id, "doc_type": doc.doc_type},
            doc_dict,
            upsert=True
        )

    async def remove_document(self, doc_id: str, doc_type: str) -> None:
        await self.collection.delete_one({"_id": doc_id, "doc_type": doc_type})

    async def search(self, query: str, doc_type: Optional[str] = None) -> List[SearchDocument]:
        filter_query = {}
        if doc_type:
            filter_query["doc_type"] = doc_type

        # Perform case-insensitive regex pattern matching over indexed properties
        filter_query["$or"] = [
            {"title": {"$regex": query, "$options": "i"}},
            {"body": {"$regex": query, "$options": "i"}}
        ]

        cursor = self.collection.find(filter_query)
        docs = await cursor.to_list(length=100)
        return [SearchDocument(**doc) for doc in docs]

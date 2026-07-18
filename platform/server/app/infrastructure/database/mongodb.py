import logging
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)

class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.is_connected = False

db_manager = MongoDBManager()

async def connect_to_mongo():
    logger.info("Initializing async Motor client session...")
    try:
        db_manager.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )
        await db_manager.client.admin.command('ping')
        db_manager.db = db_manager.client[settings.MONGODB_DB_NAME]
        db_manager.is_connected = True
        logger.info(f"Successfully connected to MongoDB — database: {settings.MONGODB_DB_NAME}")
        return True
    except Exception as e:
        db_manager.is_connected = False
        logger.critical(f"Failed to connect to MongoDB: {e}")
        return False

async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    if db_manager.client:
        db_manager.client.close()
        db_manager.client = None
        db_manager.db = None
        db_manager.is_connected = False
        logger.info("MongoDB connection closed.")

async def get_database():
    if not db_manager.is_connected or db_manager.db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is currently unavailable."
        )
    return db_manager.db

import logging
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    client: AsyncIOMotorClient = None
    db = None

db_manager = DatabaseManager()

async def connect_to_mongo():
    logger.info("Initializing async Motor client session...")
    try:
        db_manager.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )
        # Execute ping command to verify connection
        await db_manager.client.admin.command('ping')
        db_manager.db = db_manager.client[settings.MONGODB_DB_NAME]
        logger.info(f"Successfully established connection to MongoDB Atlas database: {settings.MONGODB_DB_NAME}")
    except Exception as e:
        logger.critical(f"Failed to establish connection to MongoDB Atlas: {e}")
        raise e

async def close_mongo_connection():
    logger.info("Closing MongoDB Atlas connection...")
    if db_manager.client:
        db_manager.client.close()
        db_manager.client = None
        db_manager.db = None
        logger.info("MongoDB Atlas connection closed successfully.")

async def get_database():
    if db_manager.db is None:
        raise RuntimeError("Database client session is uninitialized. Ping verification failed.")
    return db_manager.db

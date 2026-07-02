import logging
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException, status
from core.config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    client: AsyncIOMotorClient = None
    db = None
    is_connected: bool = False

db_manager = DatabaseManager()

async def connect_to_mongo():
    """Attempt to connect to MongoDB Atlas.
    Returns True on success, False on failure.
    Does NOT raise — the caller decides how to handle failure.
    """
    logger.info("Initializing async Motor client session...")
    try:
        db_manager.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )
        # Lightweight ping to verify reachability
        await db_manager.client.admin.command('ping')
        db_manager.db = db_manager.client[settings.MONGODB_DB_NAME]
        db_manager.is_connected = True
        logger.info(
            f"Successfully connected to MongoDB Atlas — "
            f"database: {settings.MONGODB_DB_NAME}"
        )
        return True
    except Exception as e:
        db_manager.is_connected = False
        logger.critical(
            f"Failed to connect to MongoDB Atlas: {e}\n"
            f"The server will start in DEGRADED MODE. "
            f"Ensure your IP is whitelisted in Atlas Network Access."
        )
        return False

async def close_mongo_connection():
    logger.info("Closing MongoDB Atlas connection...")
    if db_manager.client:
        db_manager.client.close()
        db_manager.client = None
        db_manager.db = None
        db_manager.is_connected = False
        logger.info("MongoDB Atlas connection closed.")

async def get_database():
    """FastAPI dependency — returns the DB handle or raises HTTP 503."""
    if not db_manager.is_connected or db_manager.db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Database is currently unavailable. "
                "Ensure your IP is whitelisted in MongoDB Atlas "
                "Network Access and restart the server."
            )
        )
    return db_manager.db

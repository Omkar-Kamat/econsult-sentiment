from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


mongodb = MongoDB()


async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    mongodb.client = AsyncIOMotorClient(settings.mongodb_url)
    mongodb.db = mongodb.client[settings.mongodb_db_name]
    await mongodb.client.admin.command("ping")
    logger.info(f"Connected to MongoDB: {settings.mongodb_db_name}")
    await create_indexes()


async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
        logger.info("MongoDB connection closed.")


async def create_indexes():
    db = mongodb.db
    await db.complaints.create_index("created_at")
    await db.complaints.create_index("cluster_id")
    await db.complaints.create_index("sentiment")
    await db.complaints.create_index("session_id")
    await db.responses.create_index("complaint_id")
    await db.responses.create_index("created_at")
    await db.responses.create_index("cluster_id")
    await db.sessions.create_index("session_id", unique=True)
    await db.sessions.create_index("created_at")
    logger.info("MongoDB indexes created.")


def get_db() -> AsyncIOMotorDatabase:
    return mongodb.db
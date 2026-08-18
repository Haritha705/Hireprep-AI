from motor.motor_asyncio import AsyncIOMotorClient
import logging
import sys
import os

# Add the parent directory of this file to sys.path to allow importing config
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import MONGODB_URL, DB_NAME

# Setup Logger (Critical for Cloud Debugging)
logger = logging.getLogger("uvicorn")

class Database:
    client: AsyncIOMotorClient = None

db_instance = Database()

def get_database_client():
    return db_instance.client


def get_vector_collection():
    db_name = DB_NAME or "rag_db"
    return db_instance.client[db_name]["vector_documents"]

def question_collection():
    db_name = DB_NAME or "rag_db"
    return db_instance.client[db_name]["questions"]

def get_users_collection():
    db_name = DB_NAME or "rag_db"
    return db_instance.client[db_name]["users"]


async def connect_to_mongo():
    try:
        logger.info("⏳ Connecting to MongoDB...")
        db_instance.client = AsyncIOMotorClient(MONGODB_URL)
        
        # THE PING TEST (Crucial for Cloud)
        await db_instance.client.admin.command('ping')
        logger.info("✅ MongoDB Connected Successfully!")
    except Exception as e:
        logger.error(f"❌ MongoDB Connection Failed: {e}")
        raise e


async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        logger.info("🔒 MongoDB connection closed.")


if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    try:
        asyncio.run(connect_to_mongo())
    finally:
        asyncio.run(close_mongo_connection())
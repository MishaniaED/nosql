import os
import motor.motor_asyncio
from pymongo import MongoClient

# Asynchronous client
mongo_db = os.getenv('MONGO_DB')
async_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_db, directConnection=True)

async_db = async_client[str(mongo_db)]

# Synchronous client (for sharding configuration and other administrative tasks)
sync_client = MongoClient(os.getenv('MONGO_DB'), directConnection=True)

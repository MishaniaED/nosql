import os
import motor.motor_asyncio
from pymongo import MongoClient

# Asynchronous client
async_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017", directConnection=True)
mongo_db = os.getenv('MONGO_DB')

async_db = async_client[str(mongo_db)]

# Synchronous client (for sharding configuration and other administrative tasks)
sync_client = MongoClient(os.getenv('MONGO_DB'), directConnection=True)


def setup_sharding():
    # Select the database and the admin database
    sdb = sync_client["nosql-db"]
    admin_db = sync_client["admin"]

    # Enable sharding for the database
    #admin_db.command("enableSharding", "nosql-db")

    # Set the sharding key for the collection
    #sdb.command("shardCollection", "nosql-db", key={"station_id": 1})

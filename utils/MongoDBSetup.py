import os
import motor.motor_asyncio
from pymongo import MongoClient

# Asynchronous client
async_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
mongo_db = os.getenv('MONGO_DB')

async_db = async_client[str(mongo_db)]

# Synchronous client (for sharding configuration and other administrative tasks)
sync_client = MongoClient(os.getenv('MONGO_DB'))


def setup_sharding():
    # Select the database and the admin database
    sdb = sync_client["railway_ticket_system"]
    admin_db = sync_client["admin"]

    # Enable sharding for the database
    admin_db.command("enableSharding", "railway_ticket_system")

    # Set the sharding key for the collection
    sdb.command("shardCollection", "railway_ticket_system", key={"station_id": 1})

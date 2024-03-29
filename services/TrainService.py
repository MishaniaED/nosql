from datetime import datetime

from utils.ElasticsearchConnector import search_trains, add_train_to_index, delete_train_from_index
from utils.MongoDBSetup import async_db


class TrainService:

    @staticmethod
    async def initialize_train(train_data):
        existing_station = await async_db.trains.find_one({"id": train_data["id"]})
        if existing_station:
            return None
        await add_train_to_index(train_data)
        insert_result = await async_db.trains.insert_one(train_data)
        inserted_train = await async_db.trains.find_one({"_id": insert_result.inserted_id})

        return inserted_train

    @staticmethod
    async def get_train(train_id: int):
        result = await async_db.trains.find_one({"id": train_id})
        if result:
            return result
        return None

    @staticmethod
    async def get_available_trains(departure_station_id: int, departure_date: datetime, arrival_station_id: int):
        return search_trains(departure_station_id, arrival_station_id, departure_date)

    @staticmethod
    async def delete_train(train_id: int):
        deleted_train = await async_db.trains.delete_one({"id": train_id})
        delete_train_from_index(train_id)
        return deleted_train.deleted_count > 0

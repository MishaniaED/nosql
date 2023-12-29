from utils.HazelcastConnector import get_cached_station, cache_station
from utils.MongoDBSetup import async_db


class StationService:

    @staticmethod
    async def add_station(station_data):
        existing_station = await async_db.stations.find_one({"station_id": station_data["station_id"]})
        if existing_station:
            return None
        cache_station(station_data["station_id"], station_data)
        insert_result = await async_db.stations.insert_one(station_data)
        inserted_station = await async_db.stations.find_one({"_id": insert_result.inserted_id})

        return inserted_station

    @staticmethod
    async def get_station(station_id: int):
        result = await get_cached_station(station_id)
        if result is None:
            station = await async_db.stations.find_one({"station_id": station_id})
            if not station:
                return None
            cache_station(station["station_id"], station)
        return result

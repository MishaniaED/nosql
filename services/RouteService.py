from utils.MongoDBSetup import async_db


class RouteService:

    @staticmethod
    async def add_route(route_data):
        existing_route = await async_db.routes.find_one({"id": route_data["id"]})
        if existing_route:
            return None

        insert_result = await async_db.routes.insert_one(route_data)
        inserted_route = await async_db.routes.find_one({"_id": insert_result.inserted_id})

        return inserted_route

    @staticmethod
    async def get_route(route_id: int):
        result = await async_db.routes.find_one({"id": route_id})
        if result:
            return result
        return None

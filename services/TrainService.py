from datetime import datetime


class TrainService:

    @staticmethod
    async def initialize_train(train_data):
        pass

    @staticmethod
    async def get_train(train_id: int):
        pass

    @staticmethod
    async def get_available_trains(route_id: int, type: str, departure_date: datetime, arrival_date: datetime):
        pass

    @staticmethod
    async def delete_train(train_id: int):
        pass

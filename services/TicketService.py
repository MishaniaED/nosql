from datetime import datetime
from typing import List


class TicketService:

    @staticmethod
    async def search_tickets(train_id: int, status: str, comfort_class: str):  ### Параметры поиска
        pass

    @staticmethod
    async def book_ticket(ticket_id: int) -> bool:
        pass

    @staticmethod
    async def purchase_ticket(ticket_id: int) -> bool:
        pass

    @staticmethod
    async def get_ticket(ticket_id: int):
        pass

    @staticmethod
    async def add_ticket(ticket_data: int):
        pass

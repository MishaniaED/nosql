from datetime import datetime
from typing import List

from pymongo import ReturnDocument

from models.Ticket import Ticket
from utils.ElasticsearchConnector import search_trains
from utils.HazelcastConnector import unlock_ticket, lock_ticket
from utils.MongoDBSetup import async_db


class TicketService:

    @staticmethod
    async def search_tickets(train_id: int, status: str, comfort_class: str):
        trains = search_trains(train_id,
                               status,
                               comfort_class)
        tickets = []

        for train in trains:
            try:
                # Fetching tickets for each train from MongoDB
                train_tickets = async_db.tickets.find({"train_id": train["train_id"],
                                                       "status": "free"})
                async for ticket in train_tickets:
                    tickets.append(Ticket(**ticket))
            except Exception as e:
                raise Exception(
                    f"Error fetching tickets for train {train['train_id']}: {e}")

        return tickets

    @staticmethod
    async def book_ticket(ticket_id: int) -> bool:
        result = await async_db.tickets.find_one({"ticket_id": ticket_id})
        if not result:
            raise Exception("Ticket not found")

        if result["status"] != "free":
            raise Exception("Ticket already booked")

        if not lock_ticket(ticket_id):
            raise Exception("Failed to lock ticket")

        try:
            update_data = {"$set": {"status": "booked", "booking_time": datetime.now()}}
            updated_ticket = await async_db.tickets.find_one_and_update(
                {"ticket_id": ticket_id},
                update_data,
                return_document=ReturnDocument.AFTER
            )
            if updated_ticket:
                return True
            raise Exception("Error updating ticket")
        except Exception as e:
            raise Exception(f"Internal server error: {e}")
        finally:
            unlock_ticket(ticket_id)

    @staticmethod
    async def purchase_ticket(ticket_id: int) -> bool:
        payment_successful = True  # Placeholder
        result = await async_db.tickets.find_one({"ticket_id": ticket_id})

        if not result:
            raise Exception("Ticket not found")

        if result["status"] != 'booked':
            raise Exception("Ticket not booked")

        if payment_successful:
            try:
                update_data = {"$set": {"status": "purchased", "payment_time": datetime.now()}}
                updated_ticket = await async_db.tickets.find_one_and_update(
                    {"ticket_id": ticket_id},
                    update_data,
                    return_document=ReturnDocument.AFTER
                )

                if updated_ticket:
                    return True

                raise Exception("Error purchasing ticket")
            except Exception as e:
                raise Exception(f"Error purchasing ticket: {e}")
        else:
            raise Exception("Payment failed")

    @staticmethod
    async def get_ticket(ticket_id: int):
        result = await async_db.tickets.find_one({"ticket_id": ticket_id})
        if result:
            return result
        return None

    @staticmethod
    async def add_ticket(ticket_data):
        ticket_data.status = "free"
        ticket_data.booking_time = datetime(1, 1, 1, 0, 0, 0)
        ticket_data.payment_time = datetime(1, 1, 1, 0, 0, 0)
        existing_ticket = await async_db.tickets.find_one({"ticket_id": ticket_data.ticket_id})
        if existing_ticket:
            return None
        ticket_dict = ticket_data.dict()
        insert_result = await async_db.tickets.insert_one(ticket_dict)
        inserted_ticket = await async_db.tickets.find_one({"_id": insert_result.inserted_id})

        return inserted_ticket

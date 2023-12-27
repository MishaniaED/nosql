from datetime import datetime
from pydantic import BaseModel


class TicketPlace(BaseModel):
    ticket_id: int
    train_id: int
    seat_number: int
    status: str  # 'free', 'booked', 'purchased'
    price: float
    booking_time: datetime = None
    payment_time: datetime = None
from pydantic import BaseModel
from datetime import datetime


class Ticket(BaseModel):
    id: int
    train_id: int
    status: str
    price: float
    passenger_data: str     # John Smith
    comfort_class: str      # Economy, business
    carriage_number: int    # Wagon number
    seat_number: int
    booking_date: datetime = None
    payment_date: datetime = None

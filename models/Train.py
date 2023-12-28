from pydantic import BaseModel
from datetime import datetime


class Train(BaseModel):
    id: int
    route_id: int
    type: str  # Lastochka
    departure_date: datetime
    arrival_date: datetime

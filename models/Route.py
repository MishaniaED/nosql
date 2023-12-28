from datetime import datetime
from pydantic import BaseModel
from typing import List


class Route(BaseModel):
    id: int
    name: str
    travel_time: datetime
    travel_distance: int
    stations_id: List[int]

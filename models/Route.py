from datetime import datetime
from pydantic import BaseModel
from typing import List


class Route(BaseModel):
    id: int
    stations_id: List[int]
    name: str
    type: str # tourist express freight
    travel_time: datetime
    travel_distance: int

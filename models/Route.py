from typing import List
from pydantic import BaseModel


class Route(BaseModel):
    route_id: int
    route_name: str
    stations: List[int]  # station_id-s


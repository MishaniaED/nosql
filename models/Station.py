from pydantic import BaseModel


class Station(BaseModel):
    id: int
    country_name: str
    area_name: str
    name: str

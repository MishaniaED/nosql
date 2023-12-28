from fastapi import APIRouter, HTTPException
from models.Station import Station
from services.StationService import StationService

router = APIRouter()


@router.post("/", response_model=Station, responses={
    409: {"description": "A station with this ID already exists"}
})
async def add_station(station_data: Station):
    station_model_dump = station_data.model_dump()
    result = await StationService.add_station(station_model_dump)

    if result is not None:
        return result

    raise HTTPException(status_code=409, detail="A station with this ID already exists")


@router.get("/{station_id}", response_model=Station, responses={
    404: {"description": "The station was not found"},
    500: {"description": "Server error"},
})
async def get_station(station_id: int):
    result = await StationService.get_station(station_id)

    if result is not None and not isinstance(result, Exception):
        return Station(**result)

    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail="Server error")

    raise HTTPException(status_code=404, detail="The station was not found")


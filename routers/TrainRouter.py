from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from models.Train import Train
from services.TrainService import TrainService

router = APIRouter()


@router.post("/", response_model=Train, responses={
    409: {"description": "Train with this ID already exists"}
})
async def add_train(train_data: Train):
    train_model_dump = train_data.model_dump()
    result = await TrainService.initialize_train(train_model_dump)

    if result is None:
        raise HTTPException(status_code=409, detail="Train with this ID already exists")

    return Train(**result)


@router.get("/{train_id}", response_model=Train, responses={
    404: {"description": "Train not found"},
    500: {"description": "Server error"},
})
async def get_train(train_id: int):
    result = await TrainService.get_train(train_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Train not found")

    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail="Server error")

    return Train(**result)


@router.get("/available/", response_model=List[Train])
async def available_trains(route_id: int, type: str, departure_date: datetime, arrival_date: datetime):
    results = await TrainService.get_available_trains(route_id, type, departure_date, arrival_date)

    return [Train(**result) for result in results]


@router.delete("/{train_id}/", responses={
    404: {"description": "Train not found"},
})
async def delete_train(train_id: int):
    success = await TrainService.delete_train(train_id)

    if success:
        return {"message": "Train deleted successfully"}

    raise HTTPException(status_code=404, detail="Train not found")

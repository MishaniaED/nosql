from fastapi import APIRouter, HTTPException
from models.Route import Route
from services.RouteService import RouteService

router = APIRouter()


@router.post("/", response_model=Route, responses={
    409: {"description": "A route with this ID already exists"}
})
async def add_route(route_data: Route):
    route_model_dump = route_data.model_dump()
    result = await RouteService.add_route(route_model_dump)

    if result is not None:
        return result

    raise HTTPException(status_code=409, detail="A route with this ID already exists")


@router.get("/{route_id}", response_model=Route, responses={
    404: {"description": "The route was not found"},
})
async def get_route(route_id: int):
    result = await RouteService.get_route(route_id)

    if result is not None:
        return result

    raise HTTPException(status_code=404, detail="The route was not found")

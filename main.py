from fastapi import FastAPI
import uvicorn

import routers.RouteRouter
from handler.EventHandlers import startup, shutdown
from routers import RouteRouter, StationRouter, TrainRouter, TicketRouter


app = FastAPI()

app.add_event_handler("startup", startup)

app.include_router(StationRouter.router, prefix="/station", tags=["Stations"])
app.include_router(RouteRouter.router, prefix="/route", tags=["Routes"])
app.include_router(TrainRouter.router, prefix="/train", tags=["Trains"])
app.include_router(TicketRouter.router, prefix="/ticket", tags=["Tickets"])

# app.add_event_handler("shutdown", shutdown)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)

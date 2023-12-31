from fastapi import FastAPI
import uvicorn

from handler.EventHandlers import startup, shutdown

app = FastAPI()

# app.add_event_handler("startup", startup)
# app.add_event_handler("shutdown", shutdown)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)

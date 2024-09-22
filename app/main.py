import uvicorn
from fastapi import FastAPI

from app.config import config
from app.routers import init_api_routers

app = FastAPI(title="Pimple Tracker", version="0.1")

init_api_routers(app)

if __name__ == "__main__":
    uvicorn.run(app="main:app", **config.uvicorn.model_dump())

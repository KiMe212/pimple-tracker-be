from fastapi import FastAPI

from .pimple import router as pimple_router


def init_api_routers(app: FastAPI) -> None:
    app.include_router(pimple_router, tags=["Pimple"])

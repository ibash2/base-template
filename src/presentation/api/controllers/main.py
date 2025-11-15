from fastapi import FastAPI

from .default import default_router
from .healthcheck import healthcheck_router
from .example.handlers import router as example_router
from .exceptions import setup_exception_handlers


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(healthcheck_router)
    app.include_router(example_router)
    setup_exception_handlers(app)

from contextlib import asynccontextmanager

from fastapi import FastAPI

from presentation.api.controllers.main import setup_controllers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def init_api() -> FastAPI:
    app = FastAPI(
        title="Tron Account Service",
        docs_url="/api/docs",
        description="Simple tron account info service",
        debug=True,
        lifespan=lifespan,
    )
    setup_controllers(app)

    return app

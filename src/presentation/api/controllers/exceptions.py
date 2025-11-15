import logging
from collections.abc import (
    Awaitable,
    Callable,
)

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from fastapi.responses import JSONResponse

from domain.common.exceptions.base import AppError
from presentation.api.controllers.schemas import ErrorSchema

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, error_handler())
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler() -> Callable[..., Awaitable[JSONResponse]]:
    return app_error_handler


async def app_error_handler(
    request: Request, err: AppError,
) -> JSONResponse:
    return await handle_error(request=request, err=err, err_data=err.message)


async def unknown_exception_handler(request: Request, err: Exception) -> JSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return JSONResponse(
        ErrorSchema(error=err.__class__.__name__),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_data: str,
) -> JSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return JSONResponse(
        content=ErrorSchema(error=err_data).model_dump(),
        status_code=400,
    )

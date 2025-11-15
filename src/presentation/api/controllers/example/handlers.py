from typing import Annotated

from fastapi import (
    Depends,
    Query,
    status,
)
from fastapi.routing import APIRouter

from infrastructure.init import resolve_mediator
from infrastructure.mediator.base import Mediator
from presentation.api.controllers.schemas import ErrorSchema
from application.example.queries.example import GetExampleInfoQuery, GetExamplesQuery
from presentation.api.controllers.example.schemas import ExampleInfoDetail, GetExampleInfoRequest, GetExampleInfoResponse, GetExamplesQueryResponse


router = APIRouter(tags=["Account"], prefix="/account")


@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт возвращает список всех alert",
    responses={
        status.HTTP_200_OK: {"model": GetExamplesQueryResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_alerts_handler(
    mediator: Mediator = Depends(resolve_mediator),
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1)] = 1000,
):
    examples, count = await mediator.handle_query(
        GetExamplesQuery(
            offset=offset,
            limit=limit,
        ),
    )
    return GetExamplesQueryResponse(
        count=count,
        items=[ExampleInfoDetail.from_entity(alert) for alert in examples],
    )


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт отдает данные по аддресу",
    responses={
        status.HTTP_200_OK: {"model": GetExampleInfoResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_account_info_handler(
    request: GetExampleInfoRequest,
    mediator: Mediator = Depends(resolve_mediator),
) -> GetExampleInfoResponse:
    account_info = await mediator.handle_query(
        GetExampleInfoQuery(
            address=request.address,
        ),
    )

    return GetExampleInfoResponse.from_dto(account_info)

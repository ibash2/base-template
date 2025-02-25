from typing import Annotated
from punq import Container
from fastapi import (
    Depends,
    Query,
    status,
)
from fastapi.routing import APIRouter

from presentation.api.controllers.account.schemas import (
    AccountDetailSchema,
    GetAccountInfoRequestSchema,
    GetAccountInfoResponseSchema,
    GetAccountsQueryResponseSchema,
)
from presentation.api.controllers.schemas import ErrorSchema

from application.commands.account import GetAccountInfoCommand
from application.queries.account import GetAccountInfoQuery, GetAccountsQuery
from infrastructure.init import init_container
from infrastructure.mediator.base import Mediator


router = APIRouter(tags=["Account"], prefix="/account")


@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт возвращает список всех alert",
    responses={
        status.HTTP_200_OK: {"model": GetAccountsQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_alerts_handler(
    container: Container = Depends(init_container),
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1)] = 1000,
):
    mediator: Mediator = container.resolve(Mediator)  # type: ignore

    alerts, count = await mediator.handle_query(
        GetAccountsQuery(
            offset=offset,
            limit=limit,
        ),
    )
    return GetAccountsQueryResponseSchema(
        count=count,
        items=[AccountDetailSchema.from_entity(alert) for alert in alerts],
    )


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт отдает данные по аддресу",
    responses={
        status.HTTP_200_OK: {"model": GetAccountInfoResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_account_info_handler(
    schema: GetAccountInfoRequestSchema,
    container: Container = Depends(init_container),
) -> GetAccountInfoResponseSchema:
    mediator: Mediator = container.resolve(Mediator)  # type: ignore

    account_info = await mediator.handle_query(
        GetAccountInfoQuery(
            address=schema.address,
        ),
    )

    return GetAccountInfoResponseSchema.from_entity(account_info)

from functools import lru_cache

from application.account.commands.account import GetAccountInfoCommand, GetAccountInfoCommandHandler
from application.account.queries.account import (
    GetAccountInfoQuery,
    GetAccountInfoQueryHandler,
    GetAccountsQuery,
    GetAccountsQueryHandler,
)
from application.common.interfaces.uow import UnitOfWork
from httpx import AsyncClient
from infrastructure.persistence.db.repositories.address import BaseAccountRepository, SqlAlchemyAccountRepository
from infrastructure.persistence.db.repositories.base import build_sa_engine, build_sa_session_factory
from infrastructure.persistence.db.uow import SQLAlchemyUoW
from tronpy.async_tron import AsyncTron, AsyncHTTPProvider
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)
from punq import (
    Container,
    Scope,
)

from settings.config import Config
from infrastructure.integrations.blockchain.clients.base import BaseAccountDataClient
from infrastructure.integrations.blockchain.clients.tron import TronAccountDataClient
from infrastructure.mediator.base import Mediator
from infrastructure.mediator.command import CommandMediator
from infrastructure.mediator.event import EventMediator
from infrastructure.mediator.query import QueryMediator


@lru_cache(1)
def init_container() -> Container:
    return _init_container()

def resolve_mediator() -> Mediator:
    container = init_container()
    return container.resolve(Mediator)

def _init_container() -> Container:
    container = Container()

    # Configs
    container.register(Config, instance=Config())  # type: ignore
    config: Config = container.resolve(Config)  # type: ignore

    # Integrations
    container.register(
        BaseAccountDataClient,
        instance=TronAccountDataClient(
            AsyncTron(
                AsyncHTTPProvider(
                    config.tron_rpc_url,
                    api_key=config.tron_rpc_api_key,
                ),
            )
        ),
    )

    # Repositories
    container.register(
        AsyncEngine,
        instance=build_sa_engine(config),
        scope=Scope.singleton,
    )
    container.register(
        async_sessionmaker[AsyncSession],
        instance=build_sa_session_factory(container.resolve(AsyncEngine)),
        scope=Scope.singleton,
    )
    container.register(SQLAlchemyUoW, SQLAlchemyUoW)
    container.register(UnitOfWork, SQLAlchemyUoW)

    container.register(BaseAccountRepository, SqlAlchemyAccountRepository)

    # Mediator
    mediator = Mediator(container)

    # commands
    mediator.register_command(GetAccountInfoCommand, GetAccountInfoCommandHandler)

    # queries
    mediator.register_query(GetAccountsQuery, GetAccountsQueryHandler)
    mediator.register_query(GetAccountInfoQuery, GetAccountInfoQueryHandler)

    container.register(Mediator, instance=mediator)
    container.register(EventMediator, instance=mediator)
    container.register(QueryMediator, instance=mediator)
    container.register(CommandMediator, instance=mediator)

    return container

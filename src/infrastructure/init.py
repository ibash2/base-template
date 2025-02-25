from functools import lru_cache

from httpx import AsyncClient
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
from application.queries.account import (
    GetAccountInfoQuery,
    GetAccountInfoQueryHandler,
    GetAccountsQuery,
    GetAccountsQueryHandler,
)
from application.commands.account import (
    GetAccountInfoCommandHandler,
    GetAccountInfoCommand,
)
from infrastructure.integrations.blockchain.clients.base import BaseAccountDataClient
from infrastructure.integrations.blockchain.clients.tron import TronAccountDataClient
from infrastructure.db.repositories.address import (
    BaseAccountRepository,
    SqlAlchemyAccountRepository,
)
from infrastructure.db.repositories.base import (
    build_sa_engine,
    build_sa_session_factory,
)
from infrastructure.db.uow import SQLAlchemyUoW

from infrastructure.uow import UnitOfWork
from infrastructure.mediator.base import Mediator
from infrastructure.mediator.command import CommandMediator
from infrastructure.mediator.event import EventMediator
from infrastructure.mediator.query import QueryMediator


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


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
    container.register(SQLAlchemyUoW, SQLAlchemyUoW, scope=Scope.singleton)
    container.register(UnitOfWork, SQLAlchemyUoW, scope=Scope.singleton)

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

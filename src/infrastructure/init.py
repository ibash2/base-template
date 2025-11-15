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
from application.common.interfaces.uow import UnitOfWork
from application.example.interfaces.persistence.repo import ExampleRepo
from application.example.interfaces.persistence.reader import ExampleInfoReader
from application.example.commands.example import CreateExampleCommand, CreateExampleCommandHandler
from application.example.queries.example import GetExampleInfoQuery, GetExampleInfoQueryHandler, GetExamplesQuery, GetExamplesQueryHandler
from infrastructure.persistence.db.uow import SQLAlchemyUoW
from infrastructure.persistence.db.repositories.example import SqlAlchemyExampleRepo
from infrastructure.integrations.blockchain.clients.tron import TronExampleInfoReader
from infrastructure.persistence.db.repositories.base import build_sa_engine, build_sa_session_factory
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
        ExampleInfoReader,
        instance=TronExampleInfoReader(
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

    container.register(ExampleRepo, SqlAlchemyExampleRepo)

    # Mediator
    mediator = Mediator(container)

    # commands
    mediator.register_command(CreateExampleCommand, CreateExampleCommandHandler)

    # queries
    mediator.register_query(GetExamplesQuery, GetExamplesQueryHandler)
    mediator.register_query(GetExampleInfoQuery, GetExampleInfoQueryHandler)

    container.register(Mediator, instance=mediator)
    container.register(EventMediator, instance=mediator)
    container.register(QueryMediator, instance=mediator)
    container.register(CommandMediator, instance=mediator)

    return container

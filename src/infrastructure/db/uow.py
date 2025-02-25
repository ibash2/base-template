import logging
from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)


logger = logging.getLogger(__name__)


@dataclass
class SQLAlchemyUoW:
    _session_factory: async_sessionmaker[AsyncSession]

    async def __aenter__(self):
        self._session = await self._session_factory().__aenter__()  # type: ignore
        return self._session

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._session.rollback()
        await self._session.close()

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError:
            logger.exception("Error during commit")
            # raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError:
            logger.exception("Error during rollback")
            # raise RollbackError from err

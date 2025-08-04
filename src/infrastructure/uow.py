from collections.abc import Sequence
from typing import Protocol

from infrastructure.persistence.db.uow import SQLAlchemyUoW


def build_uow(db_uow: SQLAlchemyUoW) -> "UnitOfWorkImpl":
    uow = UnitOfWorkImpl((db_uow,))
    return uow


class UnitOfWorkImpl:
    def __init__(self, uows: Sequence[]) -> None:
        self._uows = uows

    async def __aenter__(self):
        for uow in self._uows:
            await uow.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        for uow in self._uows:
            await uow.__aexit__(exc_type, exc_value, traceback)

    async def commit(self) -> None:
        for uow in self._uows:
            await uow.commit()

    async def rollback(self) -> None:
        for uow in self._uows:
            await uow.rollback()

from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select, or_, and_
from domain.entities.account import Account

from infrastructure.db import models
from infrastructure.db.converters import (
    convert_account_entity_to_db_model,
    convert_db_model_to_account_entity,
)
from infrastructure.db.repositories.base import SQLAlchemyRepo


@dataclass
class BaseAccountRepository(SQLAlchemyRepo, ABC):
    @abstractmethod
    async def add_account(self, account: Account) -> None: ...

    @abstractmethod
    async def get_accounts(
        self, offset: int, limit: int
    ) -> tuple[Iterable[Account], int]: ...


@dataclass
class SqlAlchemyAccountRepository(BaseAccountRepository):
    async def add_account(self, account: Account) -> None:
        db_account = convert_account_entity_to_db_model(account)
        self._session.add(db_account)
        try:
            await self._session.flush((db_account,))
        except Exception as e:
            return ValueError("Sql Error")

    async def get_accounts(
        self, offset: int, limit: int
    ) -> tuple[Iterable[Account], int]:
        stmt = select(models.Account).offset(offset).limit(limit)
        db_accounts = await self._session.scalars(stmt)

        return map(convert_db_model_to_account_entity, db_accounts), len(db_accounts)

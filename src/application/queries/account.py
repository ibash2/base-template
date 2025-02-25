from dataclasses import dataclass
from typing import Iterable

from application.queries.base import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.entities.account import Account, AccountInfo
from domain.values.address import Address
from infrastructure.uow import UnitOfWork
from infrastructure.db.repositories.address import BaseAccountRepository
from infrastructure.integrations.blockchain.clients.base import BaseAccountDataClient


@dataclass(frozen=True)
class GetAccountsQuery(BaseQuery):
    offset: int | None
    limit: int | None


@dataclass(frozen=True)
class GetAccountInfoQuery(BaseQuery):
    address: str


@dataclass(frozen=True)
class GetAccountsQueryHandler(
    BaseQueryHandler[GetAccountsQuery, tuple[Iterable[Account], int]]
):
    uow: UnitOfWork
    account_repository: BaseAccountRepository

    async def handle(self, query: GetAccountsQuery) -> tuple[Iterable[Account], int]:
        async with self.uow as session:
            self.account_repository._session = session
            accounts, count = await self.account_repository.get_accounts(
                query.offset, query.limit
            )

        return accounts, count


@dataclass(frozen=True)
class GetAccountInfoQueryHandler(BaseQueryHandler[GetAccountInfoQuery, AccountInfo]):
    uow: UnitOfWork
    account_repository: BaseAccountRepository
    wallet_data_client: BaseAccountDataClient

    async def handle(self, query: GetAccountInfoQuery) -> AccountInfo:
        address = Address(value=query.address)
        wallet_info = await self.wallet_data_client.get_address_info(address)

        async with self.uow as session:
            self.account_repository._session = session
            account = Account.create(address)
            await self.account_repository.add_account(account)

            await self.uow.commit()

        return wallet_info

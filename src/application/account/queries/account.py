from dataclasses import dataclass
from typing import Iterable

from application.common.query import (
    Query,
    QueryHandler,
)
from application.common.interfaces.uow import UnitOfWork


from domain.account.entities.account import Account, AccountInfo
from domain.account.value_objects.address import Address
from infrastructure.integrations.blockchain.clients.base import BaseAccountDataClient
from infrastructure.persistence.db.repositories.address import BaseAccountRepository


@dataclass(frozen=True)
class GetAccountsQuery(Query):
    offset: int | None
    limit: int | None


@dataclass(frozen=True)
class GetAccountInfoQuery(Query):
    address: str


@dataclass(frozen=True)
class GetAccountsQueryHandler(
    QueryHandler[GetAccountsQuery, tuple[Iterable[Account], int]]
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
class GetAccountInfoQueryHandler(QueryHandler[GetAccountInfoQuery, AccountInfo]):
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

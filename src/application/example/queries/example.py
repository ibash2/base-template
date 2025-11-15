from dataclasses import dataclass
from typing import Iterable

from application.common.query import (
    Query,
    QueryHandler,
)
from application.common.interfaces.uow import UnitOfWork


from application.example import dto
from domain.example.entities.example import Example
from domain.example.value_objects.address import Address
from application.example.interfaces.persistence.repo import ExampleRepo
from application.example.interfaces.persistence.reader import ExampleInfoReader


@dataclass(frozen=True)
class GetExamplesQuery(Query):
    offset: int | None
    limit: int | None


@dataclass(frozen=True)
class GetExampleInfoQuery(Query):
    address: str


@dataclass(frozen=True)
class GetExamplesQueryHandler(
    QueryHandler[GetExamplesQuery, tuple[Iterable[Example], int]]
):
    uow: UnitOfWork
    example_repo: ExampleRepo

    async def handle(self, query: GetExamplesQuery) -> tuple[Iterable[Example], int]:
        async with self.uow:
            accounts, count = await self.example_repo.get_accounts(query.offset or 0, query.limit or 100)

        return accounts, count


@dataclass(frozen=True)
class GetExampleInfoQueryHandler(QueryHandler[GetExampleInfoQuery,  dto.ExampleInfo]):
    uow: UnitOfWork
    wallet_data_reader: ExampleInfoReader
    example_repo: ExampleRepo

    async def handle(self, query: GetExampleInfoQuery) -> dto.ExampleInfo:
        address = Address(value=query.address)
        example_info = await self.wallet_data_reader.get_address_info(address)

        if not example_info: 
            raise ValueError("Account not found") # TODO Cahnge to custom exception

        async with self.uow :
            account = Example.create(address)
            await self.example_repo.add_account(account)

            await self.uow.commit()

        return example_info

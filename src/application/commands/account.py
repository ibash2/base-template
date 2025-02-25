from dataclasses import dataclass

from application.commands.base import (
    BaseCommand,
    CommandHandler,
)
from domain.entities.account import Account, AccountInfo
from domain.values.address import Address
from infrastructure.uow import UnitOfWork
from infrastructure.db.repositories.address import BaseAccountRepository
from infrastructure.integrations.blockchain.clients.base import BaseAccountDataClient


@dataclass(frozen=True)
class GetAccountInfoCommand(BaseCommand):
    address: str


@dataclass(frozen=True)
class GetAccountInfoCommandHandler(CommandHandler[GetAccountInfoCommand, AccountInfo]):
    uow: UnitOfWork
    account_repository: BaseAccountRepository
    wallet_data_client: BaseAccountDataClient

    async def handle(self, command: GetAccountInfoCommand) -> AccountInfo:
        address = Address(value=command.address)
        wallet_info = await self.wallet_data_client.get_address_info(address)

        async with self.uow as session:
            self.account_repository._session = session
            account = Account.create(address)
            await self.account_repository.add_account(account)

            await self.uow.commit()

        return wallet_info

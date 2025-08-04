from dataclasses import dataclass

from application.common.interfaces.uow import UnitOfWork
from application.common.command import Command, CommandHandler
from domain.account.entities.account import Account, AccountInfo
from domain.account.value_objects.address import Address
from infrastructure.integrations.blockchain.clients.base import BaseAccountDataClient
from infrastructure.persistence.db.repositories.address import BaseAccountRepository


@dataclass(frozen=True)
class GetAccountInfoCommand(Command):
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

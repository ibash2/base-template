from dataclasses import (
    dataclass,
    field,
)

from tronpy.async_tron import AsyncTron

from domain.entities.account import AccountInfo
from domain.values.address import Address
from infrastructure.integrations.blockchain.clients.base import BaseAccountDataClient


@dataclass()
class TronAccountDataClient(BaseAccountDataClient):
    client: AsyncTron

    async def get_address_info(self, address: Address) -> AccountInfo | None:
        account_info = await self.client.get_account(address.as_generic_type())
        # account_resource = await self.client.get_account_resource(address)

        return AccountInfo(
            balance=account_info["balance"],
            bandwidth=account_info["net_window_size"],
            energy=account_info["account_resource"]["energy_window_size"],
        )

from dataclasses import dataclass

from tronpy.async_tron import AsyncTron

from application.example import dto
from domain.example.value_objects.address import Address
from application.example.interfaces.persistence.reader import ExampleInfoReader

@dataclass()
class TronExampleInfoReader(ExampleInfoReader):
    client: AsyncTron

    async def get_address_info(self, address: Address) -> dto.ExampleInfo | None:
        account_info = await self.client.get_account(address.as_generic_type())
 
        if not account_info:    
            return None
        
        return dto.ExampleInfo(
            balance=account_info["balance"],
            bandwidth=account_info["net_window_size"],
            energy=account_info["account_resource"]["energy_window_size"],
        )

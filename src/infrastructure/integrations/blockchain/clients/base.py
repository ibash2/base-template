from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.account import AccountInfo
from domain.values.address import Address


@dataclass
class BaseAccountDataClient(ABC):
    @abstractmethod
    async def get_address_info(self, address: Address) -> AccountInfo | None: ...

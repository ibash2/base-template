import abc
from typing import Protocol

from application.example import dto
from domain.example.value_objects.address import Address


class ExampleInfoReader(Protocol):
    @abc.abstractmethod
    async def get_address_info(self, address: Address) -> dto.ExampleInfo | None: ...

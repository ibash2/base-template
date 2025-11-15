from dataclasses import dataclass

from domain.common.entities import Entity
from domain.example.value_objects.address import Address


@dataclass
class Example(Entity):
    address: Address

    @classmethod
    def create(cls, address: Address):
        return cls(address=address)


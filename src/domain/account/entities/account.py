from dataclasses import dataclass

from domain.common.entities import Entity
from domain.account.value_objects.address import Address


@dataclass
class Account(Entity):
    address: Address

    @classmethod
    def create(cls, address: Address):
        return cls(address=address)


@dataclass
class AccountInfo(Entity):
    balance: int
    energy: int
    bandwidth: int

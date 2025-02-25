from dataclasses import dataclass
from domain.entities.base import BaseEntity
from domain.values.address import Address


@dataclass
class Account(BaseEntity):
    address: Address

    @classmethod
    def create(cls, address: str):
        return cls(address=address)


@dataclass
class AccountInfo(BaseEntity):
    balance: int
    energy: int
    bandwidth: int

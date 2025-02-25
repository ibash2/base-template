from dataclasses import dataclass

from domain.exceptions.account import NoValidAddressException
from domain.values.base import ValueObject


@dataclass(frozen=True)
class Address(ValueObject[str]):
    def validate(self):
        if not self.value:
            raise NoValidAddressException()
        if len(self.value) != 34:
            raise NoValidAddressException()

    def as_generic_type(self) -> str:
        return self.value

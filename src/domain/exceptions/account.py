from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class NoValidAddressException(ApplicationException):
    @property
    def message(self):
        return "Tron address is not valid"

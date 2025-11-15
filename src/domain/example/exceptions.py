from dataclasses import dataclass

from domain.common.exceptions import DomainError


@dataclass(eq=False)
class NoValidAddressException(DomainError):
    
    @property
    def message(self):
        return "Tron address is not valid"

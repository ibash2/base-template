from abc import ABC
from typing import Optional

from dataclasses import dataclass

class DTO(ABC):
    pass


@dataclass
class TokenInfo(DTO):
    address: str
    name: str
    symbol: str
    description: Optional[str] 
    image: str
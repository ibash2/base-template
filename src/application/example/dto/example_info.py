from dataclasses import dataclass

from application.common.dto import DTO


@dataclass
class ExampleInfo(DTO):
    balance: int
    energy: int
    bandwidth: int

from decimal import Decimal
from dataclasses import dataclass
from typing import TypeAlias

from application.common.dto import DTO
from application.common.pagination.dto import PaginatedItemsDTO


@dataclass
class Transaction(DTO):
    address: str
    signer: str
    signature: str

    price: Decimal
    price_usd: Decimal

    total_usd: Decimal
    base_amount: Decimal
    quote_amount: Decimal

    is_buy: bool
    created_at: int


PaginatedTransactions: TypeAlias = PaginatedItemsDTO[Transaction]

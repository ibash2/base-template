from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from application.common.dto import DTO
from domain.common.constants import Empty

Item = TypeVar("Item")


class OrderBy(Enum):
    CREATED_AT = "created_at"
    MARKET_CAP = "market_cap"
    LIQUIDITY = "liquidity"
    VOLUME = "volume"


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True)
class Pagination:
    """Pagination parameters"""

    limit: int
    offset: int = 0


@dataclass(frozen=True)
class Sorting:
    """Sorting parameters"""

    order_by: OrderBy
    direction: SortDirection = SortDirection.ASC


@dataclass(frozen=True)
class QueryParameters:
    """Query parameters"""

    pagination: Pagination
    sorting: Sorting


@dataclass(frozen=True)
class PaginationResult(DTO):
    offset: int | None
    limit: int | None
    # total: int
    # order: SortDirection

    @classmethod
    def from_pagination(cls, pagination: Pagination) -> "PaginationResult":
        offset = pagination.offset if pagination.offset is not Empty.UNSET else None
        limit = pagination.limit if pagination.limit else None
        return cls(offset=offset, limit=limit)
    
    @classmethod
    def empty(cls) -> "PaginationResult":
        return cls(None, None) 
    


@dataclass(frozen=True)
class PaginatedItemsDTO(DTO, Generic[Item]):
    data: list[Item]
    pagination: PaginationResult

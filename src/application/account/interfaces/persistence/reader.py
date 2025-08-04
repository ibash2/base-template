from decimal import Decimal
from typing import Protocol

from application.account import dto
from application.common.pagination.dto import Pagination, QueryParameters


class TransactionsReader(Protocol): 
    async def get_transactions_by_pair(self, address: str, pagination: Pagination) -> dto.PaginatedTransactions:
        raise NotImplementedError
    
    async def get_transactions_stats_by_pair(self, address: str): 
        raise NotImplementedError

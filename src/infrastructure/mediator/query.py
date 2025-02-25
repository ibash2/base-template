from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)

from application.queries.base import (
    BaseQuery,
    BaseQueryHandler,
    QR,
    QT,
)


@dataclass(eq=False)
class QueryMediator(ABC):
    queries_map: dict[QT, type[BaseQueryHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(self, query: QT, query_handler: type[BaseQueryHandler[QT, QR]]) -> QR:
        ...

    @abstractmethod
    async def handle_query(self, query: BaseQuery) -> QR:
        ...

from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from application.common.event import (
    Event,
    EventHandler,
    ER,
    ET,
)


@dataclass(eq=False)
class EventMediator(ABC):
    events_map: dict[ET, list[type[EventHandler]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_event(
        self, event: ET, event_handler: type[EventHandler[ET, ER]], **kwargs
    ): ...

    @abstractmethod
    async def publish(self, events: Iterable[Event]) -> Iterable[ER]: ...

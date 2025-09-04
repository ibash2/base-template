from abc import ABC
from dataclasses import dataclass, field

from domain.common.events.event import Event

from .entity import Entity


@dataclass
class AggregateRoot(Entity, ABC):
    # id: UUID = field(default_factory=uuid4, kw_only=True)
    _events: list[Event] = field(default_factory=list, init=False, repr=False, hash=False, compare=False)
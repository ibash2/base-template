from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Generic,
    TypeVar,
)


VT = TypeVar("VT", bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self): ...


@dataclass(frozen=True)
class ValueObject(BaseValueObject, ABC, Generic[VT]):
    value: VT

    @abstractmethod
    def as_generic_type(self) -> VT: ...

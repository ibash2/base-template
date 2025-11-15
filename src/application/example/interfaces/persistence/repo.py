import abc
from typing import Iterable, Protocol

from domain.example.entities.example import Example


class ExampleRepo(Protocol):
    @abc.abstractmethod
    async def add_account(self, example: Example) -> None: ...

    @abc.abstractmethod
    async def get_accounts(
        self, offset: int, limit: int
    ) -> tuple[Iterable[Example], int]: ...

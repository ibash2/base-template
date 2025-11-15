from dataclasses import dataclass

from application.common.interfaces.uow import UnitOfWork
from application.common.command import Command, CommandHandler


@dataclass(frozen=True)
class CreateExampleCommand(Command):
    address: str


@dataclass(frozen=True)
class CreateExampleCommandHandler(CommandHandler[CreateExampleCommand, None]):
    uow: UnitOfWork

    async def handle(self, command: CreateExampleCommand) -> None:
        pass
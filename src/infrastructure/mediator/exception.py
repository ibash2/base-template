from dataclasses import dataclass


@dataclass(eq=False)
class MediatorException(Exception):
    @property
    def message(self):
        return "Ощибка инициализации медиатора."


@dataclass(eq=False)
class EventHandlersNotRegisteredException(MediatorException):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для события: {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(MediatorException):
    command_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для команды: {self.command_type}"

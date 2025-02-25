import logging
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    asdict,
    dataclass,
    field,
)

from punq import Container

from application.commands.base import (
    BaseCommand,
    CommandHandler,
    CR,
    CT,
)
from application.events.base import (
    BaseEvent,
    EventHandler,
    ER,
    ET,
)
from application.queries.base import (
    BaseQuery,
    BaseQueryHandler,
    QR,
    QT,
)
from infrastructure.mediator.command import CommandMediator
from infrastructure.mediator.event import EventMediator
from infrastructure.mediator.query import QueryMediator


logger = logging.getLogger("mediator")


@dataclass(eq=False)
class Mediator(EventMediator, QueryMediator, CommandMediator):
    container: Container
    events_map: dict[ET, list[type[EventHandler]]] = field(  # type: ignore
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CT, list[type[CommandHandler]]] = field(  # type: ignore
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[QT, type[BaseQueryHandler]] = field(  # type: ignore
        default_factory=dict,
        kw_only=True,
    )

    def register_event(
        self,
        event: type[ET],
        event_handler: type[EventHandler[ET, ER]],
        **kwargs,
    ):
        self.container.register(event_handler, event_handler, **kwargs)
        self.events_map[event].append(event_handler)

    def register_command(
        self,
        command: type[CT],
        command_handler: type[CommandHandler[CT, CR]],
    ):
        self.container.register(command_handler)
        self.commands_map[command].append(command_handler)

    def register_query(
        self,
        query: type[QT],
        query_handler: type[BaseQueryHandler[QT, QR]],
    ) -> QR:  # type: ignore
        self.container.register(query_handler)
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            logger.debug(f"{event} occurred", extra={"event_data": asdict(event)})
            handlers: Iterable[type[EventHandler]] = self.events_map[event.__class__]
            result.extend(
                [
                    await self.container.resolve(handler).handle(event)  # type: ignore
                    for handler in handlers
                ],
            )

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)
        logger.debug(f"{command} occurred", extra={"event_data": asdict(command)})

        # if not handlers:
        #     raise CommandHandlersNotRegisteredException(command_type)

        return [
            await self.container.resolve(handler).handle(command)  # type: ignore
            for handler in handlers
        ]

    async def handle_query(self, query: BaseQuery) -> QR:
        logger.debug(f"{query} occurred", extra={"event_data": asdict(query)})
        return await self.container.resolve(self.queries_map[query.__class__]).handle(  # type: ignore
            query=query,
        )

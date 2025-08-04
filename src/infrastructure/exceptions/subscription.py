from dataclasses import dataclass

from infrastructure.exceptions.base import InfrastructureException


@dataclass(eq=False)
class SubscriptionNotFoundException(InfrastructureException):

    @property
    def message(self):
        return "Subscription not found"


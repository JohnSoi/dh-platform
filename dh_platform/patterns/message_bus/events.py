from typing import Any, Type
from uuid import UUID, uuid4

from pydantic import BaseModel


class Event(BaseModel):
    """
    Базовый класс события

    Examples:
        >>> class UserCreatedEvent(Event):
        ...     user_id: str
        ...     email: str
    """

    @property
    def uuid(self) -> UUID:
        return uuid4()


class EventHandler:
    """
    Обработчик события

    Examples:
        >>> class UserCreatedHandler(EventHandler):
        >>> async def handle(self, event: UserCreatedEvent):
        ...     print(f"User created: {event.email}")
    """

    async def handle(self, event: Event) -> Any:
        raise NotImplementedError


EventType = Type[Event]


__all__: list[str] = ["Event", "EventType", "EventHandler"]

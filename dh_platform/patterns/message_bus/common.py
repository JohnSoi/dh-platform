import logging
from collections import defaultdict
from typing import Dict, List

from .events import Event, EventHandler, EventType

logger = logging.getLogger("dh_logger")


class MessageBus:
    """Глобальная шина событий"""

    def __init__(self):
        self._subscriptions: Dict[EventType, List[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """
        Регистрация обработчика для типа события

        Args:
            event_type: тип события
            handler: обработчик

        Examples:
            >>> from dh_platform.patterns.message_bus import message_bus
            >>>
            >>> message_bus.subscribe(UserCreatedEvent, UserCreatedHandler())
        """
        logger.info(f"Подписка на события с типом {event_type}")
        self._subscriptions[event_type].append(handler)

    async def publish(self, event: Event) -> None:
        """
        Публикация события всем подписчикам

        Args:
            event: Данные события

        Examples:
            >>> from dh_platform.patterns.message_bus import message_bus
            >>>
            >>> event = UserCreatedEvent(user_id="123", email="test@example.com")
            >>> await message_bus.publish(event)
        """
        logger.info(f"Публикация события с данными {event}")
        handlers = self._subscriptions.get(type(event), [])
        for handler in handlers:
            await handler.handle(event)


message_bus = MessageBus()

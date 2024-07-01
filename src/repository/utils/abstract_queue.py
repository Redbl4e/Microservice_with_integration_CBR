from abc import abstractmethod
from typing import Any, Callable


class AbstractQueueRepository:
    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def declare_queue(self, queue_name: str):
        raise NotImplementedError

    @abstractmethod
    async def send_message(self, queue_name: str, message: Any):
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError

    @abstractmethod
    async def consume_messages(self, queue_name: str, callback: Callable[[Any], None]):
        raise NotImplementedError

import aio_pika
from aio_pika.exceptions import AMQPException

import json
from typing import Any, Callable

from src.core.config.settings import settings
from src.repository.exceptions import RepositoryException
from src.repository.utils.abstract_queue import AbstractQueueRepository


class RabbitMQ(AbstractQueueRepository):
    def __init__(self, url: str | None = None):
        self.url = url if url else settings.RABBITMQ.RABBITMQ_URL
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def declare_queue(self, queue_name: str):
        return await self.channel.declare_queue(queue_name, durable=True)

    async def send_message(self, queue_name: str, message: Any):
        try:
            queue = await self.declare_queue(queue_name)
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(message).encode('utf-8')),
                routing_key=queue.name,
            )
        except AMQPException:
            raise RepositoryException

    async def close(self):
        await self.connection.close()

    async def consume_messages(self, queue_name: str, callback: Callable[[Any], None]):
        queue = await self.declare_queue(queue_name)
        await queue.consume(
            lambda msg: callback(json.loads(msg.body.decode('utf-8'))), no_ack=True
        )


rabbit_mq = RabbitMQ()

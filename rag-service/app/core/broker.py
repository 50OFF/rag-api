#app/core/broker.py

import json
import asyncio
import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection, AbstractChannel
from abc import ABC, abstractmethod
from typing import Callable, Awaitable


class Broker(ABC):
    @abstractmethod
    async def connect(self):
        ...

    @abstractmethod
    async def produce(self, queue_name: str, message: dict):
        ...

    @abstractmethod
    async def consume(self, queue_name: str, message_callback: Callable):
        ...

    @abstractmethod
    async def close(self):
        ...


class RabbitMQClient(Broker):
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url: str = rabbitmq_url
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractChannel | None = None

    async def connect(self) -> None:
        "Connect to RabbitMQ."
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()

    async def ensure_connection(self) -> None:
        "Ensure connection to RabbitMQ."
        if self.connection is None or self.connection.is_closed:
            await self.connect()

    async def produce(self, queue_name: str, message: dict) -> None:
        "Publish message in queue."
        await self.ensure_connection()

        if self.channel is None:
            raise RuntimeError("RabbitMQ channel is not initialized")
        
        await self.channel.declare_queue(queue_name)

        await self.channel.default_exchange.publish(
            Message(body=json.dumps(message).encode("utf-8")),
            routing_key=queue_name
        )

    async def consume(self, queue_name: str, message_callback: Callable[[AbstractIncomingMessage], Awaitable]) -> None:
        "Consume messages from queue."
        await self.ensure_connection()

        if self.channel is None:
            raise RuntimeError("RabbitMQ channel is not initialized")

        queue = await self.channel.declare_queue(queue_name)

        await queue.consume(message_callback)
    
    async def close(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()

        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            
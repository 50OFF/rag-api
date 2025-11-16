#app/core/rabbitmq.py

import json
import asyncio
import aio_pika
from aio_pika import Message
from app.core.logger import logger

class RabbitMQClient:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
    
    async def connect(self):
        if self.connection is not None:
            await self.connection.close()
            self.channel = None
        
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()

    async def produce(self, queue_name: str = None, message: dict = None):
        if queue_name is None:
            logger.warning("Queue is not defined to produce message.")
            return
        
        if message is None:
            logger.warning("Message is not defined.")
            return
        
        await self.channel.declare_queue(queue_name)

        await self.channel.default_exchange.publish(
            Message(body=json.dumps(message).encode("utf-8")),
            routing_key=queue_name
        )
    
    async def consume(self, queue_name: str = None, message_callback = None):
        if queue_name is None:
            logger.warning("Queue is not defined to consume.")
            return
        
        if message_callback is None:
            logger.warning("Message callback is not defined.")
            return
    
        queue = await self.channel.declare_queue(queue_name)

        await queue.consume(message_callback)

        await asyncio.Future()

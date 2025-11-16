import aio_pika
import json


class RabbitMQClient():
    def __init__(self, rabbitmq_url: str = None):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None

    async def initialize(self):
        await self.ensure_connecion()

    async def ensure_connecion(self):
        if self.connection is None or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
            self.channel = await self.connection.channel()
            
    async def publish_message(self, queue_name: str = None, message: dict = None):
        if queue_name == None:
            print('queue name is None')
            return

        if message is None:
            message = {"message": "none"}

        await self.ensure_connecion()

        await self.channel.declare_queue(queue_name)
        
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=queue_name
        )

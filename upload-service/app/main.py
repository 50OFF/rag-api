#app/main.py

import asyncio
from app.core.config import settings
from app.core.rabbitmq import RabbitMQClient
from app.consumers import upload

async def main():
    rabbit = RabbitMQClient(settings.rabbitmq_url)
    await rabbit.connect()

    await rabbit.consume(settings.upload_queue, lambda msg: upload.handle(rabbit, msg))

if __name__ == "__main__":
    asyncio.run(main())
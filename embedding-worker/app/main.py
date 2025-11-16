import asyncio
from app.services.rabbitmq_client import RabbitMQClient
from app.core.config import settings
from app.worker import on_message
from app.services import db

async def main():
    db_pool = await db.get_db_pool()

    rabbit = RabbitMQClient(settings.rabbitmq_url)
    await rabbit.connect()
    await rabbit.consume(settings.embedding_queue, lambda msg: on_message(msg, db_pool))

    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

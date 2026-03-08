#app/main.py

import asyncio
from app.core.broker import RabbitMQClient
from app.core.config import settings
from app.core.logger import logger
from app.services.db import DataBase
from app.services.embedder import Embedder
from app.consumers import chunks

async def main():
    logger.info("Embedding service started.")
    embedder = Embedder()

    db = DataBase(settings.postgres_host,
                    settings.postgres_port,
                    settings.postgres_user,
                    settings.postgres_password,
                    settings.postgres_db)
    await db.connect()

    rabbit = RabbitMQClient(settings.rabbitmq_url)
    await rabbit.connect()
    
    await rabbit.consume(settings.chunks_queue, lambda msg: chunks.handle(embedder, db, msg))

if __name__ == "__main__":
    asyncio.run(main())

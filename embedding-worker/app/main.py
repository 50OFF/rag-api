#app/main.py

import asyncio
from app.core.broker import RabbitMQClient
from app.core.config import settings
from app.services.db import DataBase
from app.services.embedder import Embedder
from app.consumers import embedding

async def main():
    embedder = Embedder()

    db = DataBase(settings.postgres_host,
                    settings.postgres_port,
                    settings.postgres_user,
                    settings.postgres_password,
                    settings.postgres_db)
    await db.connect()

    rabbit = RabbitMQClient(settings.rabbitmq_url)
    await rabbit.connect()
    
    await rabbit.consume(settings.embedding_queue, lambda msg: embedding.handle(embedder, db, msg))


if __name__ == "__main__":
    asyncio.run(main())

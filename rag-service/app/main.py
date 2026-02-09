#app/main.py

import asyncio
from app.core.broker import RabbitMQClient
from app.core.config import settings
from app.services.db import DataBase
from app.services.embedder import Embedder
from app.consumers import rag
import signal

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

    stop_event = asyncio.Event()

    def _signal_handler(*_):
        stop_event.set()
    
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, _signal_handler)
    loop.add_signal_handler(signal.SIGTERM, _signal_handler)

    consumer_task = asyncio.create_task(rabbit.consume(settings.rag_queue, lambda msg: rag.handle(rabbit, embedder, db, msg)))

    await stop_event.wait()
    consumer_task.cancel()
    await rabbit.close()
    await db.close()

if __name__ == "__main__":
    asyncio.run(main())

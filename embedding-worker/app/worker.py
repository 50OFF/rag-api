import json
import aio_pika
from app.services.embedder import Embedder
from app.services.db import get_db_pool
from app.core.config import settings
from app.core.logger import logger
from pgvector.asyncpg import register_vector

embedder = Embedder()

async def on_message(message: aio_pika.IncomingMessage, db_pool):
    async with message.process():
        data = json.loads(message.body.decode("utf-8"))

        chunk_id = data["chunk_id"]
        file_id = data["file_id"]
        user_id = data["user_id"]
        text = data["text"]

        logger.debug(f"Got chunk {chunk_id}")

        embedding = embedder.generate(text)

        async with db_pool.acquire() as conn:
            await register_vector(conn)
            await conn.execute(
                """
                INSERT INTO embeddings (chunk_id, file_id, user_id, text, embedding)
                VALUES ($1, $2, $3, $4, $5)
                """,
                chunk_id, file_id, user_id, text, embedding,
            )

        logger.debug(f"Saved embedding for {chunk_id}")

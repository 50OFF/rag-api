#app/consumers/embedding.py

import json
from aio_pika import IncomingMessage
from app.services.embedder import Embedder
from app.services.db import DataBase
from app.core.logger import logger

async def handle(embedder: Embedder, db: DataBase, message: IncomingMessage):
    "Handle imcoming message about creating embeddings."
    try:
        async with message.process():
            data = json.loads(message.body.decode())

            chunk_id = data["chunk_id"]
            file_id = data["file_id"]
            user_id = data["user_id"]
            text = data["text"]

            logger.debug(f"Got chunk {chunk_id}")

            embedding = await embedder.generate_embedding(text)

            await db.insert_embedding(chunk_id, file_id, user_id, text, embedding)

            logger.debug(f"Saved embedding for {chunk_id}")
    
    except Exception as e:
        logger.exception(f"Error in message callback: {e}")
        await message.nack()
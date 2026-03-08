#app/consumers/embedding.py

import json
from aio_pika import IncomingMessage
from app.services.embedder import Embedder
from app.services.db import DataBase
from app.core.logger import logger
from app.models.chunks import Chunk

async def handle(embedder: Embedder, db: DataBase, message: IncomingMessage):
    "Handle imcoming message about creating embeddings."
    logger.info("Recieved file chunked event.")
    try:
        async with message.process():
            data = json.loads(message.body.decode())
            chunk = Chunk(**data)

            logger.debug(f"Got chunk {chunk.chunk_id} of file {chunk.file_id}")

            embedding = await embedder.generate_embedding(chunk.text)

            await db.insert_embedding(chunk.chunk_id, chunk.file_id, chunk.user_id, chunk.text, embedding)

            logger.info(f"Saved embedding for {chunk.chunk_id} of file {chunk.file_id}")
    
    except Exception as e:
        logger.exception(f"Error in message callback: {e}")
        await message.nack()
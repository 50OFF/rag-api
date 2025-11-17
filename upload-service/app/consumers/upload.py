#app/consumers/upload.py

import json
from aio_pika import IncomingMessage
from app.models.events import UploadEvent, EmbeddingEvent
from app.services.file_processing import process_uploaded_file
from app.producers.embeddings import publish_embeddings
from app.core.broker import Broker
from app.core.logger import logger

async def handle(broker: Broker, message: IncomingMessage):
    "Handle incoming message about uploading file."
    try:
        async with message.process():
            data = json.loads(message.body.decode())
            upload_event = UploadEvent(**data)

            embedding_event: EmbeddingEvent | None = await process_uploaded_file(upload_event)

            if embedding_event:
                await publish_embeddings(broker, embedding_event)
    
    except Exception as e:
        logger.exception(f"Error in message callback: {e}")
        await message.nack()
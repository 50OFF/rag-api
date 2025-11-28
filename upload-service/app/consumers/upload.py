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
    logger.info("Recieved UPLOAD message.")
    try:
        async with message.process():
            data = json.loads(message.body.decode())
            upload_event = UploadEvent(**data)

            logger.info(f"Processing file {upload_event.file_name}...")

            embedding_event: EmbeddingEvent | None = await process_uploaded_file(upload_event)

            if embedding_event:
                await publish_embeddings(broker, embedding_event)
                logger.info(f"Sent EMBEDDINGS message for file {upload_event.file_name}.")
    
    except Exception as e:
        logger.error(f"Error in processing incoming message: {e}")
        await message.nack()
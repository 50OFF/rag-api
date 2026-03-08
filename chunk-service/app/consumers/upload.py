#app/consumers/upload.py

import json
from aio_pika import IncomingMessage
from app.models.events import FileUploadedEvent, FileChunkedEvent
from app.services.file_processing import process_uploaded_file
from app.producers.chunks import publish_file_chunked_event
from app.core.broker import Broker
from app.core.logger import logger

async def handle(broker: Broker, message: IncomingMessage):
    "Handle incoming message about uploading file."
    logger.info("Recieved file uploaded event.")
    try:
        async with message.process():
            data = json.loads(message.body.decode())
            file_uploaded_event = FileUploadedEvent(**data)

            logger.info(f"Processing file {file_uploaded_event.file_name}...")

            file_chunked_event: FileChunkedEvent | None = await process_uploaded_file(file_uploaded_event)

            if file_chunked_event:
                await publish_file_chunked_event(broker, file_chunked_event)
                logger.info(f"Published file chunked event for file {file_uploaded_event.file_name}.")
    
    except Exception as e:
        logger.error(f"Error in processing incoming message: {e}")
        await message.nack()
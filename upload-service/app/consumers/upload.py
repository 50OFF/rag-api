#app/consumers/upload.py

import json
from aio_pika import Message
from app.models.events import UploadEvent, EmbeddingEvent
from app.services.file_processing import process_uploaded_file

async def handle(rabbit, msg: Message):
    data = json.loads(msg.body.decode())
    upload_event = UploadEvent(**data)

    await process_uploaded_file(rabbit, upload_event)

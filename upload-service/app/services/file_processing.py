#app/services/file_processing.py

import os
import uuid
from app.models.events import UploadEvent, EmbeddingEvent
from app.core.logger import logger
from app.core.config import settings
from app.producers.embeddings import publish_embeddings

async def process_uploaded_file(rabbit, upload_event: UploadEvent):
    file_url = upload_event.file_url
    file_id = upload_event.file_id
    user_id = upload_event.user_id

    if not os.path.exists(file_url):
        logger.error("File not found.")
        return
    
    text = ""
    with open(file_url, "r") as f:
        text = f.read()

    if not text.strip():
        logger.warning("File is empty.")
        return

    text_chunks = []
    for i in range(0, len(text), settings.chunk_size):
        chunk_text = text[i : i + settings.chunk_size]
        chunk_id = str(uuid.uuid4())

        text_chunks.append({
            "chunk_id": chunk_id,
            "file_id": file_id,
            "user_id": user_id,
            "text": chunk_text
        })

    embedding_event = EmbeddingEvent(
        file_id=file_id,
        text_chunks=text_chunks,
        user_id=user_id
    )

    await publish_embeddings(rabbit, embedding_event)
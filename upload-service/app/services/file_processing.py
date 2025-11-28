#app/services/file_processing.py

import uuid
from app.models.events import UploadEvent, EmbeddingEvent
from app.core.config import settings
from app.services.file_reader import load_text_from_file

async def process_uploaded_file(upload_event: UploadEvent):
    "Process file to create embedding event."
    file_name = upload_event.file_name
    file_id = upload_event.file_id
    user_id = upload_event.user_id

    text = load_text_from_file(file_name)

    if not text.strip():
        return None

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

    return embedding_event
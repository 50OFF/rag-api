#app/services/file_processing.py

import uuid
from app.models.events import FileUploadedEvent, FileChunkedEvent
from app.models.chunks import Chunk
from app.core.config import settings
from app.services.file_reader import load_text_from_file

async def process_uploaded_file(file_uploaded_event: FileUploadedEvent):
    "Process file to create embedding event."
    file_name = file_uploaded_event.file_name
    file_id = file_uploaded_event.file_id
    user_id = file_uploaded_event.user_id

    text = load_text_from_file(file_name)

    if not text.strip():
        return None

    text_chunks = []
    for i in range(0, len(text), settings.chunk_size):
        chunk_text = text[i : i + settings.chunk_size]
        chunk_id = str(uuid.uuid4())

        chunk_dict = {
            "chunk_id": chunk_id,
            "file_id": file_id,
            "user_id": user_id,
            "text": chunk_text
        }

        chunk = Chunk(**chunk_dict)

        text_chunks.append(chunk)

    file_chunked_event = FileChunkedEvent(
        file_id=file_id,
        text_chunks=text_chunks,
        user_id=user_id
    )

    return file_chunked_event
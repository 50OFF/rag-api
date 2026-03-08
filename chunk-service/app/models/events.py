#app/models/events.py

from pydantic import BaseModel
from .chunks import Chunk

class FileUploadedEvent(BaseModel):
    file_id: str
    file_name: str
    user_id: str

class FileChunkedEvent(BaseModel):
    file_id: str
    text_chunks: list[Chunk]
    user_id: str

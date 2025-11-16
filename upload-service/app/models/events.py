#app/models/events.py

from pydantic import BaseModel

class UploadEvent(BaseModel):
    file_id: str
    file_url: str
    user_id: str

class EmbeddingEvent(BaseModel):
    file_id: str
    text_chunks: list[dict]
    user_id: str

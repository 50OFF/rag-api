#app/models/events.py

from pydantic import BaseModel

class FileUploadedEvent(BaseModel):
    file_id: str
    file_name: str
    user_id: str

class FileChunkedEvent(BaseModel):
    file_id: str
    text_chunks: list[dict]
    user_id: str

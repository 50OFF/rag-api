#app/models/chunks.py

from pydantic import BaseModel

class Chunk(BaseModel):
    chunk_id: str
    file_id: str
    user_id: str
    text: str
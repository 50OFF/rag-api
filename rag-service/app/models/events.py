#app/models/events.py

from pydantic import BaseModel
from .chunks import Chunk


class RagEvent(BaseModel):
    question: str
    user_id: str
    top_k: int


class LlmEvent(BaseModel):
    question: str
    chunks: list[Chunk]
    
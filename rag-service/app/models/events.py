#app/models/events.py

from pydantic import BaseModel


class RagEvent(BaseModel):
    question: str
    user_id: str
    top_k: int


class LlmEvent(BaseModel):
    question: str
    chunks: list[dict]
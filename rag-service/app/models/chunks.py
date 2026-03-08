#app/models/chunks

from pydantic import BaseModel


class Chunk(BaseModel):
    id: str
    text: str
    score: float    

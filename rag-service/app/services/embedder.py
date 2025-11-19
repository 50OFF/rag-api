#app/services/embedder.py

from openai import AsyncOpenAI
from app.core.config import settings

class Embedder:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_embeddings_model

    async def embed(self, text: str) -> list[float]:
        "Create embedding for specified text."
        response = await self.client.embeddings.create(
            model=self.model,
            input=text
        )
        embedding = response.data[0].embedding
        return embedding
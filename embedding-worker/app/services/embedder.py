from openai import OpenAI
from app.core.config import settings

class Embedder:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_embeddings_model

    def generate(self, text: str) -> list[float]:
        """
        Генерирует векторное представление текста
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        embedding = response.data[0].embedding
        return embedding

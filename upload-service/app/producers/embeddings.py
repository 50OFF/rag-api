from app.models.events import EmbeddingEvent
from app.core.config import settings

async def publish_embeddings(rabbit, event: EmbeddingEvent):
    for chunk in event.text_chunks:
        await rabbit.produce(settings.embedding_queue, chunk)

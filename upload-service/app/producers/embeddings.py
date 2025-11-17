#app/producers/embeddings.py

from app.models.events import EmbeddingEvent
from app.core.config import settings
from app.core.broker import Broker

async def publish_embeddings(broker: Broker, event: EmbeddingEvent):
    "Send message about creating embeddings."
    for chunk in event.text_chunks:
        await broker.produce(settings.embedding_queue, chunk)

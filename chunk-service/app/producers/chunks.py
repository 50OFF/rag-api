#app/producers/embeddings.py

from app.models.events import FileChunkedEvent
from app.core.config import settings
from app.core.broker import Broker

async def publish_file_chunked_event(broker: Broker, event: FileChunkedEvent):
    "Send message with file chunks."
    for chunk in event.text_chunks:
        await broker.produce(settings.embedding_queue, chunk)

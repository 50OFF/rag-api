#app/consumers/rag.py

import json
from aio_pika.abc import AbstractIncomingMessage
from app.models.events import RagEvent, LlmEvent
from app.producers.llm import publish_llm_event
from app.core.broker import Broker
from app.services.db import DataBase
from app.services.embedder import Embedder
from app.services.search import rag_search

async def handle(broker: Broker, embedder: Embedder, db: DataBase, message: AbstractIncomingMessage):
    "Handle incoming message about vector search."
    async with message.process():
        data = json.loads(message.body.decode())
        rag_event = RagEvent(**data)

        chunks = await rag_search(embedder, db, rag_event)

        if chunks is None:
            raise RuntimeError("Failed to find chunks.")
        
        llm_event = LlmEvent(
            question=rag_event.question,
            chunks=chunks
        )
        
        await publish_llm_event(broker, llm_event)

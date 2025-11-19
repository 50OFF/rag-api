#app/consumers/rag.py

import json
from aio_pika import IncomingMessage
from app.models.events import RagEvent, LlmEvent
from app.producers.llm import publish_llm_event
from app.core.broker import Broker
from app.core.logger import logger
from app.services.db import DataBase
from app.services.embedder import Embedder
from app.services.search import rag_search

async def handle(broker: Broker, embedder: Embedder, db: DataBase, message: IncomingMessage):
    "Handle incoming message about uploading file."
    try:
        async with message.process():
            data = json.loads(message.body.decode())
            rag_event = RagEvent(**data)

            chunks = await rag_search(embedder, db, rag_event)

            llm_event = LlmEvent(
                question=rag_event.question,
                chunks=chunks
            )
            
            await publish_llm_event(broker, llm_event)


    except Exception as e:
        logger.exception(f"Error in message callback: {e}")
        await message.nack()
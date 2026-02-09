#app/producers/llm.py

from app.models.events import LlmEvent
from app.core.config import settings
from app.core.broker import Broker

async def publish_llm_event(broker: Broker, event: LlmEvent):
    "Send message about llm query."
    await broker.produce(settings.llm_queue, event.model_dump())
    
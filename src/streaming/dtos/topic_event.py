import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.streaming.schemas import EntitySchema, KeywordSchema, SentimentSchema
from src.utils.dates import utcnow

__all__ = ["TopicEventDTO"]


class TopicEventDTO(BaseModel):
    topic_event_uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
    content_event_uuid: uuid.UUID
    user_id: str
    keywords: list[KeywordSchema]
    entities: list[EntitySchema]
    sentiment: SentimentSchema
    timestamp: datetime = Field(default_factory=utcnow)

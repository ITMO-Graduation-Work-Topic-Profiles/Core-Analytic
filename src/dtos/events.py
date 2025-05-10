import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas import (
    EntityTopicEventSchema,
    KeywordTopicEventSchema,
    SentimentTopicEventSchema,
)
from src.utils.dates import utcnow

__all__ = [
    "ContentEventDTO",
    "TopicEventDTO",
]


class ContentEventDTO(BaseModel):
    content_event_uuid: uuid.UUID
    user_id: str
    content: str
    timestamp: datetime = Field(default_factory=utcnow)


class TopicEventDTO(BaseModel):
    topic_event_uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
    content_event_uuid: uuid.UUID
    user_id: str
    keywords: list[KeywordTopicEventSchema]
    entities: list[EntityTopicEventSchema]
    sentiment: SentimentTopicEventSchema
    timestamp: datetime = Field(default_factory=utcnow)

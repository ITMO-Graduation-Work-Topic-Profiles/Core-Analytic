import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas import (
    EntityTopicAttributesEventSchema,
    KeywordTopicAttributesEventSchema,
    SentimentTopicAttributesEventSchema,
    TopicTopicProfileEventSchema,
)
from src.utils.dates import utcnow

__all__ = [
    "ContentEventDTO",
    "TopicAttributesEventDTO",
    "TopicProfileEventDTO",
    "UserContentEventDTO",
]


class ContentEventDTO(BaseModel):
    content_event_uuid: uuid.UUID
    user_id: str
    content: str
    timestamp: datetime = Field(default_factory=utcnow)


class TopicAttributesEventDTO(BaseModel):
    topic_attributes_event_uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
    content_event_uuid: uuid.UUID
    user_id: str
    keywords: list[KeywordTopicAttributesEventSchema] = Field(default_factory=list)
    entities: list[EntityTopicAttributesEventSchema] = Field(default_factory=list)
    sentiments: list[SentimentTopicAttributesEventSchema] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=utcnow)


class TopicProfileEventDTO(BaseModel):
    topic_profile_event_uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_content_event_uuid: uuid.UUID
    user_id: str
    topics: list[TopicTopicProfileEventSchema] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=utcnow)


class UserContentEventDTO(BaseModel):
    user_content_event_uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    content_events: list[ContentEventDTO] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=utcnow)


from pydantic import BaseModel

from .entity import EntitySchema
from .keyword import KeywordSchema
from .sentiment import SentimentSchema

__all__ = ["TopicEventSchema"]


class TopicEventSchema(BaseModel):
    # user_id: str
    keywords: list[KeywordSchema]
    entities: list[EntitySchema]
    sentiment: SentimentSchema
    # timestamp: datetime = Field(default_factory=utcnow)

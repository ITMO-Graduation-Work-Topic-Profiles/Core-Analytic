from pydantic import BaseModel

__all__ = ["SentimentTopicAttributesEventSchema"]


class SentimentTopicAttributesEventSchema(BaseModel):
    name: str
    weight: float

from pydantic import BaseModel

__all__ = ["SentimentTopicEventSchema"]


class SentimentTopicEventSchema(BaseModel):
    name: str
    weight: float

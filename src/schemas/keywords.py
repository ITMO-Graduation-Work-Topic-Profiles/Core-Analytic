from pydantic import BaseModel

__all__ = ["KeywordTopicEventSchema"]


class KeywordTopicEventSchema(BaseModel):
    name: str
    weight: float

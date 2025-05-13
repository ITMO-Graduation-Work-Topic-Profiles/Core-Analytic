from pydantic import BaseModel

__all__ = ["KeywordTopicAttributesEventSchema"]


class KeywordTopicAttributesEventSchema(BaseModel):
    name: str
    weight: float

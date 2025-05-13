from pydantic import BaseModel

__all__ = ["EntityTopicAttributesEventSchema"]


class EntityTopicAttributesEventSchema(BaseModel):
    category: str
    name: str
    weight: float

from pydantic import BaseModel

__all__ = ["EntityTopicEventSchema"]


class EntityTopicEventSchema(BaseModel):
    category: str
    name: str
    weight: float

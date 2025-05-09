
from pydantic import BaseModel

__all__ = ["ContentEventSchema"]


class ContentEventSchema(BaseModel):
    user_id: str
    content: str
    # timestamp: datetime = Field(default_factory=utcnow)

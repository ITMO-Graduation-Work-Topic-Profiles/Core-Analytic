import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from src.utils.dates import utcnow

__all__ = ["ContentEventDTO"]


class ContentEventDTO(BaseModel):
    content_event_uuid: uuid.UUID
    user_id: str
    content: str
    timestamp: datetime = Field(default_factory=utcnow)

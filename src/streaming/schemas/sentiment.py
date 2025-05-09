from pydantic import BaseModel

__all__ = ["SentimentSchema"]


class SentimentSchema(BaseModel):
    name: str
    weight: float

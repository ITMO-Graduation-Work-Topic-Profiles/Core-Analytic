import typing as tp
from contextlib import asynccontextmanager

import spacy
from faststream import ContextRepo, FastStream
from faststream.kafka import KafkaBroker
from keybert import KeyBERT
from transformers import pipeline  # type: ignore[attr-defined]

from src.core import Settings
from src.streaming.routers import router

settings = Settings()


@asynccontextmanager
async def lifespan(context: ContextRepo) -> tp.AsyncGenerator[None, None]:
    context.set_global(
        "spacy_language",
        spacy.load(
            "en_core_web_sm",
            disable=["parser"],
        ),
    )
    context.set_global(
        "sentiment_pipeline",
        pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1,
            batch_size=16,
        ),
    )
    context.set_global(
        "keybert",
        KeyBERT(model="all-MiniLM-L6-v2"),
    )

    yield


broker = KafkaBroker(settings.kafka.bootstrap_servers)

broker.include_router(router)

app = FastStream(broker, lifespan=lifespan)

if __name__ == "__main__":
    pass

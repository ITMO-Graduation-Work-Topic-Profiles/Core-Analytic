import typing as tp
from contextlib import asynccontextmanager

from faststream import ContextRepo, FastStream
from faststream.kafka import KafkaBroker

from src.core import Settings
from src.pipelines import (
    BERTopicTopicsPipeline,
    KeyBERTKeywordsPipeline,
    SpacyEntitiesPipeline,
    TransformerSentimentsPipeline,
    WikipediaLabelsPipeline,
)
from src.streaming.routers import router

settings = Settings()


@asynccontextmanager
async def lifespan(context: ContextRepo) -> tp.AsyncIterator[None]:
    context.set_global("entities_pipeline", SpacyEntitiesPipeline())
    context.set_global("sentiments_pipeline", TransformerSentimentsPipeline())
    context.set_global("keywords_pipeline", KeyBERTKeywordsPipeline())
    context.set_global("topics_pipeline", BERTopicTopicsPipeline())
    context.set_global("labels_pipeline", WikipediaLabelsPipeline())

    yield


broker = KafkaBroker(settings.kafka.bootstrap_servers)

broker.include_router(router)

app = FastStream(broker, lifespan=lifespan)

if __name__ == "__main__":
    pass

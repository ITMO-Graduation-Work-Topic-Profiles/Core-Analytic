from faststream import Context
from faststream.kafka import KafkaRouter

from src.dtos import ContentEventDTO, TopicAttributesEventDTO
from src.pipelines import EntitiesPipeline, KeywordsPipeline, SentimentsPipeline
from src.streaming.transformers import (
    convert_content_to_topic_attributes_event_transformer,
)

__all__ = ["router"]


router = KafkaRouter(prefix="events-")


@router.subscriber("content")
@router.publisher("topic-attributes")
def transmit_content_event_to_topic_attributes_event_handler(
    incoming_content_event: ContentEventDTO,
    *,
    entities_pipeline: EntitiesPipeline = Context(),
    sentiments_pipeline: SentimentsPipeline = Context(),
    keywords_pipeline: KeywordsPipeline = Context(),
) -> TopicAttributesEventDTO:
    return convert_content_to_topic_attributes_event_transformer(
        incoming_content_event,
        entities=entities_pipeline.extract(incoming_content_event.content),
        sentiments=sentiments_pipeline.extract(incoming_content_event.content),
        keywords=keywords_pipeline.extract(incoming_content_event.content),
    )

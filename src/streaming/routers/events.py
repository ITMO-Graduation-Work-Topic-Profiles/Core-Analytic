from faststream import Context
from faststream.kafka import KafkaRouter

from src.dtos import ContentEventDTO, TopicAttributesEventDTO
from src.pipelines import TextAnalysisPipeline
from src.streaming.transformers import (
    convert_content_to_topic_attributes_event_transformer,
)

__all__ = ["router"]


router = KafkaRouter(prefix="events-")


@router.subscriber("content")
@router.publisher("topic-attributes")
def transmit_content_event_to_topic_attributes_event_handler(
    incoming_content_event: ContentEventDTO,
    text_analysis_pipeline: TextAnalysisPipeline = Context(),
) -> TopicAttributesEventDTO:
    data = text_analysis_pipeline.analyze(incoming_content_event.content)
    return convert_content_to_topic_attributes_event_transformer(
        incoming_content_event, data
    )

from faststream import Context
from faststream.kafka import KafkaRouter

from src.dtos import ContentEventDTO, TopicEventDTO
from src.pipelines import TextAnalysisPipeline
from src.streaming.transformers import convert_content_to_topic_event_transformer

__all__ = ["router"]


router = KafkaRouter(prefix="events-")


@router.subscriber("content")
@router.publisher("topic")
def transmit_content_to_topic_event_handler(
    incoming_content_event: ContentEventDTO,
    text_analysis_pipeline: TextAnalysisPipeline = Context(),
) -> TopicEventDTO:
    data = text_analysis_pipeline.analyze(incoming_content_event.content)
    return convert_content_to_topic_event_transformer(incoming_content_event, data)

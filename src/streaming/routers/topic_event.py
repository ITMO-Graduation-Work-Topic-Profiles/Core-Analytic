from faststream import Context
from faststream.kafka import KafkaRouter

from src.streaming.pipelines import TextAnalysisPipeline
from src.streaming.schemas import ContentEventSchema, TopicEventSchema
from src.streaming.transformers import convert_data_to_topic_event_transformer

__all__ = ["router"]


router = KafkaRouter(prefix="events-")


@router.subscriber("content")
@router.publisher("topic")
def transmit_content_to_topic_event_handler(
    content_event: ContentEventSchema,
    text_analysis_pipeline: TextAnalysisPipeline = Context(),
) -> TopicEventSchema:
    data = text_analysis_pipeline.analyze(content_event.content)
    return convert_data_to_topic_event_transformer(data)

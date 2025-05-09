from faststream import Context
from faststream.kafka import KafkaRouter

from src.streaming.pipelines import TextAnalysisPipeline
from src.streaming.schemas import ContentEventSchema, TopicEventSchema

__all__ = ["router"]

router = KafkaRouter(prefix="events-")


@router.subscriber("content")
@router.publisher("topic")
async def content_to_topic_event_handler(
    content_event: ContentEventSchema,
    text_analysis_pipeline: TextAnalysisPipeline = Context(),
) -> TopicEventSchema:
    return None

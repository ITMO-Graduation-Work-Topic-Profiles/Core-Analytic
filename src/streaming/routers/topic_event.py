from faststream.kafka import KafkaRouter

from src.streaming.schemas import ContentEventSchema, TopicEventSchema

__all__ = ["router"]

router = KafkaRouter(prefix="")


@router.subscriber("content-event")
@router.publisher("topic-event")
async def content_to_topic_event_handler(
    content_event: ContentEventSchema,
) -> TopicEventSchema:
    return None

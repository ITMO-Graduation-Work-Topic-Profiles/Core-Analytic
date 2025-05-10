from faststream.kafka import KafkaRouter

from .events import router as topic_event_router

__all__ = ["router"]

router = KafkaRouter()
router.include_router(topic_event_router)

import typing as tp

from src.streaming.schemas import TopicEventSchema

__all__ = [
    "convert_data_to_topic_event_transformer",
]


def convert_data_to_topic_event_transformer(
    data: dict[str, tp.Any],
) -> TopicEventSchema:
    return TopicEventSchema.model_validate(data)

import typing as tp

from src.dtos import ContentEventDTO, TopicEventDTO

__all__ = [
    "convert_content_to_topic_event_transformer",
]


def convert_content_to_topic_event_transformer(
    content_event: ContentEventDTO,
    topic_data: dict[str, tp.Any],
) -> TopicEventDTO:
    return TopicEventDTO.model_validate(
        {
            "user_id": content_event.user_id,
            "content_event_uuid": content_event.content_event_uuid,
            **topic_data,
        }
    )

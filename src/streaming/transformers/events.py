import typing as tp

from src.dtos import ContentEventDTO, TopicAttributesEventDTO

__all__ = [
    "convert_content_to_topic_attributes_event_transformer",
]


def convert_content_to_topic_attributes_event_transformer(
    content_event: ContentEventDTO,
    topic_attributes: dict[str, tp.Any],
) -> TopicAttributesEventDTO:
    return TopicAttributesEventDTO.model_validate(
        {
            "user_id": content_event.user_id,
            "content_event_uuid": content_event.content_event_uuid,
            **topic_attributes,
        }
    )

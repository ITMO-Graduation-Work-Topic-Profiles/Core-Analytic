import typing as tp

from src.dtos import ContentEventDTO, TopicAttributesEventDTO

__all__ = [
    "convert_content_to_topic_attributes_event_transformer",
]


def convert_content_to_topic_attributes_event_transformer(
    content_event: ContentEventDTO,
    *,
    entities: tp.Sequence[tp.Mapping[str, tp.Any]],
    sentiments: tp.Sequence[tp.Mapping[str, tp.Any]],
    keywords: tp.Sequence[tp.Mapping[str, tp.Any]],
) -> TopicAttributesEventDTO:
    return TopicAttributesEventDTO.model_validate(
        {
            "user_id": content_event.user_id,
            "content_event_uuid": content_event.content_event_uuid,
            "entities": entities,
            "sentiments": sentiments,
            "keywords": keywords,
        }
    )

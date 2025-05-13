import typing as tp

from src.dtos import (
    ContentEventDTO,
    TopicAttributesEventDTO,
    TopicProfileEventDTO,
    UserContentEventDTO,
)
from src.schemas import TopicTopicProfileEventSchema

__all__ = [
    "convert_content_to_topic_attributes_event_transformer",
    "convert_user_content_event_to_topic_profile_event_transformer",
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


def convert_user_content_event_to_topic_profile_event_transformer(
    incoming_user_content_event: UserContentEventDTO,
    *,
    topics: tp.Sequence[tp.Mapping[str, tp.Any]],
    topics_labels: tp.Sequence[tp.Sequence[tp.Mapping[str, tp.Any]]],
) -> TopicProfileEventDTO:
    topic_schemas = []
    for topic, labels in zip(topics, topics_labels):
        topic_schemas.append(
            TopicTopicProfileEventSchema.model_validate(
                {
                    "labels": labels,
                    "words": topic["words"],
                    "confidence": topic["confidence"],
                }
            )
        )

    return TopicProfileEventDTO.model_validate(
        {
            "user_content_event_uuid": incoming_user_content_event.user_content_event_uuid,
            "user_id": incoming_user_content_event.user_id,
            "topics": topic_schemas,
        }
    )

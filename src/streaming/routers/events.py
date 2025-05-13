import asyncio

from faststream import Context
from faststream.kafka import KafkaRouter

from src.dtos import (
    ContentEventDTO,
    TopicAttributesEventDTO,
    TopicProfileEventDTO,
    UserContentEventDTO,
)
from src.pipelines import (
    BERTopicTopicsPipeline,
    KeyBERTKeywordsPipeline,
    SpacyEntitiesPipeline,
    TransformerSentimentsPipeline,
    WikipediaLabelsPipeline,
)
from src.streaming.transformers import (
    convert_content_to_topic_attributes_event_transformer,
    convert_user_content_event_to_topic_profile_event_transformer,
)

__all__ = ["router"]


router = KafkaRouter(prefix="events-")


@router.subscriber("content")
@router.publisher("topicAttributes")
def transmit_content_event_to_topic_attributes_event_handler(
    incoming_content_event: ContentEventDTO,
    *,
    entities_pipeline: SpacyEntitiesPipeline = Context(),
    sentiments_pipeline: TransformerSentimentsPipeline = Context(),
    keywords_pipeline: KeyBERTKeywordsPipeline = Context(),
) -> TopicAttributesEventDTO:
    return convert_content_to_topic_attributes_event_transformer(
        incoming_content_event,
        entities=entities_pipeline.extract(incoming_content_event.content),
        sentiments=sentiments_pipeline.extract(incoming_content_event.content),
        keywords=keywords_pipeline.extract(incoming_content_event.content),
    )


@router.subscriber("userContent")
@router.publisher("topicProfile")
async def transmit_user_content_event_to_topic_profile_event_handler(
    incoming_user_content_event: UserContentEventDTO,
    *,
    topics_pipeline: BERTopicTopicsPipeline = Context(),
    labels_pipeline: WikipediaLabelsPipeline = Context(),
) -> TopicProfileEventDTO:
    topics = topics_pipeline.extract(
        [ce.content for ce in incoming_user_content_event.content_events]
    )

    topics_labels = await asyncio.gather(
        *[
            labels_pipeline.define_labels([w["name"] for w in t["words"]])
            for t in topics
        ]
    )

    return convert_user_content_event_to_topic_profile_event_transformer(
        incoming_user_content_event,
        topics=topics,
        topics_labels=topics_labels,
    )

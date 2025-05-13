import typing as tp

import hdbscan
import numpy as np
import umap
from bertopic import BERTopic
from bertopic.representation import PartOfSpeech
from bertopic.vectorizers import OnlineCountVectorizer
from sentence_transformers import SentenceTransformer

__all__ = ["BERTopicTopicsPipeline"]


class BERTopicTopicsPipeline:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        **kwargs: tp.Any,
    ) -> None:
        self._embedding_model = SentenceTransformer(model_name)
        self._min_topic_size = kwargs.get("min_topic_size", 5)
        self._umap_model_params = {
            "n_neighbors": kwargs.get("umap_model__n_neighbors", 15),
            "n_components": kwargs.get("umap_model__n_components", 10),
            "min_dist": kwargs.get("umap_model__min_dist", 0.0),
            "spread": kwargs.get("umap_model__spread", 1.0),
            "metric": kwargs.get("umap_model__metric", "cosine"),
            "init": kwargs.get("umap_model__init", "random"),
            "random_state": kwargs.get("umap_model__random_state", 42),
        }
        self._hdbscan_model_params = {
            "min_cluster_size": kwargs.get("hdbscan_model__min_cluster_size", 5),
            "min_samples": kwargs.get("hdbscan_model__min_samples", None),
            "metric": kwargs.get("hdbscan_model__metric", "euclidean"),
            "cluster_selection_method": kwargs.get(
                "hdbscan_model__cluster_selection_method", "eom"
            ),
            "cluster_selection_epsilon": kwargs.get(
                "hdbscan_model__cluster_selection_epsilon", 0.0
            ),
            "prediction_data": True,
        }
        self._vectorizer_model_params = {
            "stop_words": kwargs.get("vectorizer_model__stop_words", "english"),
            "ngram_range": kwargs.get("vectorizer_model__ngram_range", (1, 2)),
        }
        self._representation_model_params = {
            "model": kwargs.get("representation_model__model", "en_core_web_sm"),
            "pos_patterns": kwargs.get(
                "representation_model__pos_patterns",
                [
                    [{"POS": "ADJ"}, {"POS": "NOUN"}],
                    [{"POS": "ADJ"}, {"POS": "PROPN"}],
                    [{"POS": "PROPN"}, {"POS": "NOUN"}],
                    [{"POS": "NOUN"}, {"POS": "PROPN"}],
                    [{"POS": "NOUN"}],
                    [{"POS": "PROPN"}],
                ],
            ),
        }

    def extract(self, contents: tp.Sequence[str]) -> list[dict[str, tp.Any]]:
        topic_model = self._build_topic_model()

        if not contents:
            return []

        topics, probs = topic_model.fit_transform(list(contents))
        topics_info: list[dict[str, tp.Any]] = []
        for topic_id in set(topics):
            if topic_id == -1:
                continue

            words = [
                {"text": text, "score": round(score, 3)}
                for text, score in topic_model.get_topic(topic_id)
            ]

            words.sort(key=lambda x: x["score"], reverse=True)

            confidence = float(
                np.mean([p for t, p in zip(topics, probs) if t == topic_id])
            )
            topics_info.append(
                {
                    "words": words,
                    "confidence": confidence,
                }
            )

        topics_info.sort(key=lambda x: x["confidence"], reverse=True)

        return topics_info

    def _build_topic_model(self) -> BERTopic:
        return BERTopic(
            embedding_model=self._embedding_model,
            calculate_probabilities=False,
            min_topic_size=self._min_topic_size,
            umap_model=umap.UMAP(**self._umap_model_params),
            hdbscan_model=hdbscan.HDBSCAN(**self._hdbscan_model_params),
            vectorizer_model=OnlineCountVectorizer(**self._vectorizer_model_params),
            representation_model=PartOfSpeech(**self._representation_model_params),
        )

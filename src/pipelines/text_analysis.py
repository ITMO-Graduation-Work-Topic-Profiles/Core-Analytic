import collections
import typing as tp

from keybert import KeyBERT
from spacy import Language  # type: ignore[attr-defined]
from transformers import Pipeline  # type: ignore[attr-defined]

__all__ = ["TextAnalysisPipeline"]


class TextAnalysisPipeline:
    _KEEP_ENTITY_LABELS: set[str] = {
        "PERSON",
        "ORG",
        "GPE",
        "PRODUCT",
        "EVENT",
    }

    def __init__(
        self,
        spacy_language: Language,
        sentiment_pipeline: Pipeline,
        keybert: KeyBERT,
        *,
        top_n: int = 3,
    ) -> None:
        self._spacy_language = spacy_language
        self._sentiment_pipeline = sentiment_pipeline
        self._keybert = keybert
        self._top_n = top_n

    def analyze(self, content: str) -> dict[str, tp.Any]:
        sentiment = self._extract_sentiment(content)
        entities = self._extract_entities(content)
        keywords = self._extract_keywords(content)

        return {
            "sentiments": sentiment,
            "entities": entities,
            "keywords": keywords,
        }

    def _extract_sentiment(self, content: str) -> list[dict[str, tp.Any]]:
        spans = self._sentiment_pipeline(content)
        sentiments = [
            {
                "name": s["label"],
                "weight": round(s["score"], 3),
            }
            for s in spans
        ]
        return sentiments

    def _extract_entities(self, content: str) -> list[dict[str, tp.Any]]:
        doc = self._spacy_language(content)
        spans = [e for e in doc.ents if e.label_ in self._KEEP_ENTITY_LABELS]
        counts = collections.Counter([s.text for s in spans])
        total = len(doc)
        entities = [
            {
                "category": s.label_,
                "name": s.text,
                "weight": round(counts[s.text] / total, 3),
            }
            for s in spans
        ]
        return entities

    def _extract_keywords(self, content: str) -> list[dict[str, tp.Any]]:
        raw = self._keybert.extract_keywords(
            content,
            keyphrase_ngram_range=(1, 1),
            stop_words="english",
            top_n=self._top_n * 2,
        )
        keywords = []
        seen = set()
        for phrase, score in raw:
            for tok in self._spacy_language(phrase):
                lem = tok.lemma_.lower()
                if tok.pos_ in {"NOUN", "ADJ"} and len(lem) >= 4 and lem not in seen:
                    seen.add(lem)
                    keywords.append({"name": lem, "weight": round(score, 3)})
                    break
            if len(keywords) >= self._top_n:
                break
        return keywords

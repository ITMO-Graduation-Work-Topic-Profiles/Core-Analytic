import collections
import typing as tp

from keybert import KeyBERT
from spacy import Language  # type: ignore[attr-defined]
from transformers import Pipeline  # type: ignore[attr-defined]

__all__ = ["TextAnalysisPipeline"]


class TextAnalysisPipeline:
    _KEEP_ENTITY_LABELS: set[str] = {"PERSON", "ORG", "GPE", "PRODUCT", "EVENT"}

    def __init__(
        self,
        spacy_language: Language,
        sentiment_pipeline: Pipeline,
        keybert: KeyBERT,
        *,
        top_n: int = 3,
    ) -> None:
        self.spacy_language = spacy_language
        self.sentiment_pipeline = sentiment_pipeline
        self.keybert = keybert
        self.top_n = top_n

    def analyze(self, content: str) -> dict[str, tp.Any]:
        sentiment = self._extract_sentiment(content)
        entities = self._extract_entities(content)
        keywords = self._extract_keywords(content)

        return {
            "sentiment": sentiment,
            "entities": entities,
            "keywords": keywords,
        }

    def _extract_sentiment(self, content: str) -> dict[str, tp.Any]:
        s = self.sentiment_pipeline(content)[0]
        sentiment = {
            "label": s["label"],
            "score": round(s["score"], 3),
        }
        return sentiment

    def _extract_entities(self, content: str) -> list[dict[str, tp.Any]]:
        doc = self.spacy_language(content)
        spans = [e for e in doc.ents if e.label_ in self._KEEP_ENTITY_LABELS]
        counts = collections.Counter([s.text for s in spans])
        total = len(doc)
        entities = [
            {
                "name": s.text,
                "label": s.label_,
                "weight": round(counts[s.text] / total, 3),
            }
            for s in spans
        ]
        return entities

    def _extract_keywords(self, content: str) -> list[dict[str, tp.Any]]:
        raw = self.keybert.extract_keywords(
            content,
            keyphrase_ngram_range=(1, 1),
            stop_words="english",
            top_n=self.top_n * 2,
        )
        keywords = []
        seen = set()
        for phrase, score in raw:
            for tok in self.spacy_language(phrase):
                lem = tok.lemma_.lower()
                if tok.pos_ in {"NOUN", "ADJ"} and len(lem) >= 4 and lem not in seen:
                    seen.add(lem)
                    keywords.append({"keyword": lem, "score": round(score, 3)})
                    break
            if len(keywords) >= self.top_n:
                break
        return keywords

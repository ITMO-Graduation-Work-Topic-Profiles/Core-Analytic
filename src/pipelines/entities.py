import collections
import typing as tp

import spacy

__all__ = ["SpacyEntitiesPipeline"]


class SpacyEntitiesPipeline:
    def __init__(
        self,
        model_name: str = "en_core_web_sm",
        *,
        keep_entities_labels: tp.Sequence[str] | None = (
            "PERSON",
            "ORG",
            "GPE",
            "PRODUCT",
            "EVENT",
        ),
    ) -> None:
        self._spacy = spacy.load(
            model_name,
            disable=[
                "tok2vec",
                "tagger",
                "parser",
                "attribute_ruler",
                "lemmatizer",
                "textcat",
            ],
        )
        if "senter" not in self._spacy.pipe_names:
            self._add_sentecizer_pipeline()

        self._keep_entities_labels = (
            set(keep_entities_labels) if keep_entities_labels else None
        )

    def extract(self, content: str) -> list[dict[str, tp.Any]]:
        doc = self._spacy(content)

        spans = [*doc.ents]
        for name, start, end in getattr(doc._, "phrase_matches", []):
            span = doc[start:end]
            spans.append(span)

        if self._keep_entities_labels is not None:
            spans = [s for s in spans if s.label_ in self._keep_entities_labels]

        counts = collections.Counter([s.text for s in spans])
        total = len(doc)
        entities = []
        seen = set()
        for span in spans:
            text = span.text
            if (span.label_, text) in seen:
                continue
            seen.add((span.label_, text))
            entities.append(
                {
                    "category": span.label_,
                    "name": text,
                    "weight": round(counts[text] / total, 3),
                }
            )

        return entities

    def _add_sentecizer_pipeline(self) -> None:
        self._spacy.add_pipe("sentencizer")

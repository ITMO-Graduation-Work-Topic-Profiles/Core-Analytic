from spacy import Language  # type: ignore[attr-defined]
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc

__all__ = [
    "apply_phrase_matches",
]


def apply_phrase_matches(
    language: Language,
    matcher: PhraseMatcher,
    doc: Doc,
) -> Doc:
    matches = matcher(doc)
    spans = []
    for match_id, start, end in matches:
        spans.append(
            (
                language.vocab.strings[match_id],
                start,
                end,
            )
        )
    doc._.setdefault("phrase_matches", []).extend(spans)

    return doc

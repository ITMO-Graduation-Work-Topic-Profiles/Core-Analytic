import typing as tp

from keybert import KeyBERT
from sklearn.feature_extraction.text import CountVectorizer

__all__ = ["KeyBERTKeywordsPipeline"]


class KeyBERTKeywordsPipeline:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        *,
        top_n: int = 3,
        use_mmr: bool = True,
        diversity: float = 0.7,
        stopwords: str = "english",
        use_maxsum: bool = True,
        keyphrase_ngram_range: tp.Sequence[int] = (1, 2),
    ) -> None:
        self._keybert = KeyBERT(model=model_name)
        self._top_n = top_n
        self._use_mmr = use_mmr
        self._diversity = diversity
        self._stopwords = stopwords
        self._use_maxsum = use_maxsum
        self._keyphrase_ngram_range = keyphrase_ngram_range

    def extract(self, content: str) -> list[dict[str, tp.Any]]:
        keybert_keywords = self._keybert.extract_keywords(
            content,
            keyphrase_ngram_range=self._keyphrase_ngram_range,
            stop_words=self._stopwords,
            top_n=self._top_n,
            use_mmr=self._use_mmr,
            diversity=self._diversity,
            use_maxsum=self._use_maxsum,
            vectorizer=CountVectorizer(
                stop_words=self._stopwords,
            ),
        )

        keywords = []
        seen = set()
        for phrase, score in keybert_keywords:
            lemma = phrase.lower()
            if lemma not in seen:
                seen.add(lemma)
                keywords.append(
                    {
                        "name": lemma,
                        "weight": round(score, 3),
                    }
                )
            if len(keywords) >= self._top_n:
                break

        return keywords

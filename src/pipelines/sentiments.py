import typing as tp

from transformers import pipeline  # type: ignore[attr-defined]

__all__ = ["SentimentsPipeline"]


class SentimentsPipeline:
    def __init__(
        self,
        model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
        *,
        device: int = -1,
        batch_size: int = 16,
    ) -> None:
        self._pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            device=-device,
            batch_size=batch_size,
        )

    def extract(self, content: str) -> list[dict[str, tp.Any]]:
        spans = self._pipeline(content)
        sentiments = [
            {
                "name": s["label"],
                "weight": round(s["score"], 3),
            }
            for s in spans
        ]
        return sentiments

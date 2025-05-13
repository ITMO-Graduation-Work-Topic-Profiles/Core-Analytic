import asyncio
import typing
import typing as tp

import httpx
from sentence_transformers import SentenceTransformer, util

__all__ = ["WikipediaLabelsPipeline"]


class WikipediaLabelsPipeline:
    _WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self._embedding_model = SentenceTransformer(model_name)

    async def define_labels(
        self,
        words: tp.Sequence[str],
    ) -> list[dict[str, tp.Any]]:
        async with httpx.AsyncClient() as client:
            wiki_titles = await self._get_wiki_titles(
                query=self._convert_words_to_query(words),
                http_client=client,
            )

            words_embed = self._embedding_model.encode(
                " ".join(words),
                convert_to_tensor=True,
            )

            intros = await asyncio.gather(
                *[
                    self._get_wiki_intro(title, http_client=client)
                    for title in wiki_titles
                ]
            )

            labels: list[dict[str, tp.Any]] = []
            for title, intro in zip(wiki_titles, intros):
                if isinstance(intro, Exception):
                    continue
                wiki_embed = self._embedding_model.encode(
                    (intro or title)[:500],
                    convert_to_tensor=True,
                )
                score = util.cos_sim(words_embed, wiki_embed).item()
                if score > 0:
                    labels.append(
                        {
                            "text": title,
                            "score": round(score, 3),
                        }
                    )

            labels.sort(key=lambda x: x["score"], reverse=True)

            return labels

    async def _get_wiki_titles(
        self,
        query: str,
        *,
        http_client: httpx.AsyncClient,
    ) -> list[str]:
        json_data = await self._fetch_json_data_from_wiki(
            params=self._build_search_query_params(query=query),
            http_client=http_client,
        )

        titles = [item["title"] for item in json_data["query"]["search"]]

        return titles

    async def _get_wiki_intro(
        self,
        title: str,
        *,
        http_client: httpx.AsyncClient,
    ) -> str:
        json_data = await self._fetch_json_data_from_wiki(
            params=self._build_extract_query_params(title=title),
            http_client=http_client,
        )

        pages = next(iter(json_data["query"]["pages"].values()))
        intro = str(pages.get("extract", ""))

        return intro

    async def _fetch_json_data_from_wiki(
        self,
        *,
        http_client: httpx.AsyncClient,
        **kwargs: typing.Any,
    ) -> dict[str, tp.Any]:
        response = await http_client.get(
            self._WIKI_API_URL,
            **kwargs,
        )

        json_data = dict(response.json())

        return json_data

    @classmethod
    def _build_search_query_params(
        cls,
        query: str,
        limit: int = 10,
    ) -> dict[str, tp.Any]:
        return {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": limit,
        }

    @classmethod
    def _build_extract_query_params(
        cls,
        title: str,
    ) -> dict[str, tp.Any]:
        return {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": title,
            "format": "json",
        }

    @classmethod
    def _convert_words_to_query(
        cls,
        words: tp.Sequence[str],
    ) -> str:
        return " ".join(words)

from sentence_transformers import CrossEncoder

from app.config import Config


class RerankerService:
    def __init__(self):
        self.model = CrossEncoder(
            Config.RERANKER_MODEL,
            max_length=512,
        )

    def rerank(
        self,
        query,
        results,
        top_k=5,
    ):
        if not results:
            return []

        pairs = [
            (query, result["text"])
            for result in results
        ]

        scores = self.model.predict(
            pairs,
            show_progress_bar=False,
        )

        reranked = []

        for result, score in zip(results, scores):
            item = result.copy()
            item["reranker_score"] = float(score)
            reranked.append(item)

        reranked.sort(
            key=lambda item: item["reranker_score"],
            reverse=True,
        )

        return reranked[:top_k]


_reranker_service = None


def get_reranker_service():
    global _reranker_service

    if _reranker_service is None:
        _reranker_service = RerankerService()

    return _reranker_service
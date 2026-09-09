import re

from rank_bm25 import BM25Okapi


class BM25Service:
    def __init__(self):
        self.documents = []
        self.tokenized_documents = []
        self.bm25 = None

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(
            r"[A-Za-z0-9_]+",
            text.lower(),
        )

    def build_index(self, documents):
        self.documents = documents

        self.tokenized_documents = [
            self._tokenize(document.page_content)
            for document in documents
        ]

        if not self.tokenized_documents:
            self.bm25 = None
            return

        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):
        if self.bm25 is None:
            return []

        query_tokens = self._tokenize(query)

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )

        results = []

        for index in ranked_indices[:top_k]:
            results.append(
                {
                    "chunk_id": self.documents[index].metadata["chunk_id"],
                    "score": float(scores[index]),
        "           text": self.documents[index].page_content,
                    "metadata": self.documents[index].metadata,
                }
            )

        return results


_bm25_service = None


def get_bm25_service() -> BM25Service:
    global _bm25_service

    if _bm25_service is None:
        _bm25_service = BM25Service()

    return _bm25_service
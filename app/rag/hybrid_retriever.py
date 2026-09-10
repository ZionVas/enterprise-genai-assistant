from app.config import Config

from app.rag.bm25_service import get_bm25_service
from app.rag.retriever import retrieve_documents
from app.rag.rrf import reciprocal_rank_fusion


def hybrid_search(
    query: str,
    top_k: int | None = None,
    retrieval_k: int | None = None,
):

    if top_k is None:
        top_k = Config.TOP_K

    if retrieval_k is None:
        retrieval_k = Config.RETRIEVAL_K

    bm25_service = get_bm25_service()

    bm25_results = bm25_service.search(
        query=query,
        top_k=retrieval_k,
    )

    dense_results = retrieve_documents(
        query=query,
        top_k=retrieval_k,
    )

    fused_results = reciprocal_rank_fusion(
        result_lists=[
            bm25_results,
            dense_results,
        ],
        top_k=top_k,
    )

    return fused_results
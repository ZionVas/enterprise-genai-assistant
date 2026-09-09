from app.rag.bm25_service import get_bm25_service
from app.rag.retriever import retrieve_documents
from app.rag.rrf import reciprocal_rank_fusion


def hybrid_search(
    query: str,
    top_k: int = 5,
    retrieval_k: int = 10,
):

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
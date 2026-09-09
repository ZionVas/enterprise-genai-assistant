from app.rag.embedding_service import get_embedding_service
from app.rag.qdrant_service import get_qdrant_service
from app.rag.vector_store import COLLECTION_NAME


def retrieve_documents(
    query: str,
    top_k: int = 5,
):
    embedding_service = get_embedding_service()
    qdrant_service = get_qdrant_service()

    query_embedding = embedding_service.embed_query(query)

    results = qdrant_service.client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        with_payload=True,
    )

    documents = []

    for result in results.points:
        documents.append(
            {
                "score": result.score,
                "text": result.payload.get("text", ""),
                "metadata": result.payload.get("metadata", {}),
            }
        )

    return documents
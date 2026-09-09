from uuid import uuid4

from qdrant_client.models import PointStruct

from app.rag.embedding_service import get_embedding_service
from app.rag.qdrant_service import get_qdrant_service


COLLECTION_NAME = "sap_naming_rules"


def store_documents(documents):
    embedding_service = get_embedding_service()
    qdrant_service = get_qdrant_service()

    texts = [
        document.page_content
        for document in documents
    ]

    embeddings = embedding_service.embed_documents(texts)

    if not embeddings:
        return 0

    qdrant_service.create_collection(
        collection_name=COLLECTION_NAME,
        vector_size=len(embeddings[0]),
    )

    points = []

    for document, embedding in zip(documents, embeddings):
        payload = {
            "text": document.page_content,
            "metadata": document.metadata,
        }

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload=payload,
            )
        )

    qdrant_service.client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    return len(points)
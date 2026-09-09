from app.ingestion.pipeline import ingest_document
from app.rag.bm25_service import get_bm25_service


def build_bm25_index(
    file_path: str,
    category: str,
):
    documents = ingest_document(
        file_path=file_path,
        category=category,
    )

    service = get_bm25_service()

    service.build_index(documents)

    return len(documents)
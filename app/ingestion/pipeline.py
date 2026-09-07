from langchain_core.documents import Document

from app.ingestion.loaders import load_document
from app.ingestion.cleaner import clean_documents
from app.ingestion.chunker import split_documents
from app.ingestion.metadata import add_metadata


def ingest_document(
    file_path: str,
    category: str,
) -> list[Document]:

    documents = load_document(file_path)

    documents = clean_documents(documents)

    documents = add_metadata(
        documents,
        category,
    )

    chunks = split_documents(documents)

    return chunks
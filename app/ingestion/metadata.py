from pathlib import Path

from langchain_core.documents import Document


def add_metadata(
    documents: list[Document],
    category: str,
) -> list[Document]:

    enriched_documents = []

    for document in documents:
        source = Path(document.metadata.get("source", ""))

        metadata = {
            **document.metadata,
            "document_name": source.name,
            "category": category,
        }

        enriched_documents.append(
            Document(
                page_content=document.page_content,
                metadata=metadata,
            )
        )

    return enriched_documents
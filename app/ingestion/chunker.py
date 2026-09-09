import hashlib

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunk_id(document: Document, chunk_index: int) -> str:
    source = document.metadata.get("source", "")

    raw_id = f"{source}:{chunk_index}"

    return hashlib.sha256(
        raw_id.encode("utf-8")
    ).hexdigest()[:16]


def split_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index

        chunk.metadata["chunk_id"] = create_chunk_id(
            chunk,
            index,
        )

    return chunks
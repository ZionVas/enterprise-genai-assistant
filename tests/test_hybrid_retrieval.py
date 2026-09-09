from app.rag.bm25_index import build_bm25_index
from app.rag.hybrid_retriever import hybrid_search
from app.rag.vector_store import store_documents
from app.ingestion.pipeline import ingest_document


def main():

    file_path = (
        "data/documents/"
        "sap_naming_rules/"
        "demo_sap_naming_rules.txt"
    )

    chunks = ingest_document(
        file_path=file_path,
        category="sap_naming_rules",
    )

    store_documents(chunks)

    build_bm25_index(
        file_path=file_path,
        category="sap_naming_rules",
    )

    query = (
        "How should I name an internal table "
        "that is only used locally?"
    )

    results = hybrid_search(
        query=query,
        top_k=5,
        retrieval_k=10,
    )

    print("\nQUERY:")
    print(query)

    print("\nHYBRID RESULTS:")

    for index, result in enumerate(results, start=1):

        print("\n" + "=" * 60)
        print(f"RESULT {index}")
        print("=" * 60)

        print("Chunk ID:", result["chunk_id"])
        print("RRF Score:", result["rrf_score"])

        print("\nText:")
        print(result["text"])

        print("\nMetadata:")
        print(result["metadata"])


if __name__ == "__main__":
    main()
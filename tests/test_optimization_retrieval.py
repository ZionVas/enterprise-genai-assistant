from app.ingestion.pipeline import ingest_document
from app.rag.vector_store import store_documents
from app.rag.bm25_index import build_bm25_index
from app.rag.reranked_retriever import retrieve_with_reranking


def main():

    file_path = (
        "data/documents/"
        "sap_optimization_rules/"
        "demo_sap_optimization_rules.txt"
    )

    chunks = ingest_document(
        file_path=file_path,
        category="sap_optimization_rules",
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    store_documents(chunks)

    build_bm25_index(
        file_path=file_path,
        category="sap_optimization_rules",
    )

    query = """
    How can I optimize ABAP code that performs
    SELECT statements inside a LOOP and uses
    unnecessary database calls?
    """

    results = retrieve_with_reranking(
        query=query,
        top_k=5,
        retrieval_k=10,
    )

    print("\n" + "=" * 70)
    print("OPTIMIZATION RETRIEVAL RESULTS")
    print("=" * 70)

    for index, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"\nRESULT {index}"
        )

        print(
            "RRF Score:",
            result.get("rrf_score"),
        )

        print(
            "Reranker Score:",
            result.get("reranker_score"),
        )

        print(
            "\nText:"
        )

        print(
            result["text"]
        )

        print(
            "\nMetadata:"
        )

        print(
            result["metadata"]
        )


if __name__ == "__main__":
    main()
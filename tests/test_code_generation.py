from app.ingestion.pipeline import ingest_document
from app.rag.vector_store import store_documents
from app.rag.bm25_index import build_bm25_index
from app.services.code_generation_graph import build_code_generation_graph


def main():

    file_path = (
        "data/documents/"
        "sap_naming_rules/"
        "demo_sap_naming_rules.txt"
    )

    # Ingest document
    chunks = ingest_document(
        file_path=file_path,
        category="sap_naming_rules",
    )

    # Store in Qdrant
    store_documents(chunks)

    # Build BM25 index
    build_bm25_index(
        file_path=file_path,
        category="sap_naming_rules",
    )

    # Build LangGraph
    graph = build_code_generation_graph()

    # User request
    result = graph.invoke(
        {
            "user_request": (
                "Create ABAP code that reads customer records "
                "into a local internal table."
            ),
            "language": "ABAP",
            "retrieved_context": "",
            "sources": [],
            "response": "",
        }
    )

    print("\n" + "=" * 70)
    print("RETRIEVED SOURCES")
    print("=" * 70)

    print(result["response"])

    for source in result["sources"]:
        print(source)


if __name__ == "__main__":
    main()
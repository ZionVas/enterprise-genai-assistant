from app.ingestion.pipeline import ingest_document
from app.rag.vector_store import store_documents
from app.rag.bm25_index import build_bm25_index
from app.services.sap_naming_graph import (
    build_sap_naming_graph,
)


def main():

    rules_file = (
        "data/documents/"
        "sap_naming_rules/"
        "demo_sap_naming_rules.txt"
    )

    chunks = ingest_document(
        file_path=rules_file,
        category="sap_naming_rules",
    )

    store_documents(chunks)

    build_bm25_index(
        file_path=rules_file,
        category="sap_naming_rules",
    )

    with open(
        "data/test_data/sample_abap.txt",
        "r",
        encoding="utf-8",
    ) as file:

        original_code = file.read()

    graph = build_sap_naming_graph()

    result = graph.invoke(
        {
            "original_code": original_code,
            "retrieved_context": "",
            "sources": [],
            "corrected_code": "",
        }
    )

    print("\n" + "=" * 70)
    print("ORIGINAL ABAP CODE")
    print("=" * 70)

    print(original_code)

    print("\n" + "=" * 70)
    print("CORRECTED ABAP CODE")
    print("=" * 70)

    print(result["corrected_code"])

    print("\n" + "=" * 70)
    print("RETRIEVED SOURCES")
    print("=" * 70)

    for source in result["sources"]:
        print(source)


if __name__ == "__main__":
    main()
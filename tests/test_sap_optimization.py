from app.ingestion.pipeline import ingest_document
from app.rag.vector_store import store_documents
from app.rag.bm25_index import build_bm25_index

from app.services.sap_optimization_graph import (
    build_sap_optimization_graph,
)


def main():

    rules_file = (
        "data/documents/"
        "sap_optimization_rules/"
        "demo_sap_optimization_rules.txt"
    )

    chunks = ingest_document(
        file_path=rules_file,
        category="sap_optimization_rules",
    )

    store_documents(chunks)

    build_bm25_index(
        file_path=rules_file,
        category="sap_optimization_rules",
    )

    with open(
        "data/test_data/"
        "sample_abap_optimization.txt",
        "r",
        encoding="utf-8",
    ) as file:

        original_code = file.read()

    graph = build_sap_optimization_graph()

    result = graph.invoke(
        {
            "original_code": original_code,
            "retrieved_context": "",
            "sources": [],
            "optimized_code": "",
            "validation_errors": [],
            "iteration": 0,
            "validation_passed": False,
        }
    )

    print("\n" + "=" * 70)
    print("ORIGINAL ABAP")
    print("=" * 70)

    print(original_code)

    print("\n" + "=" * 70)
    print("OPTIMIZED ABAP")
    print("=" * 70)

    print(result["optimized_code"])

    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)

    print(
        "Passed:",
        result["validation_passed"],
    )

    print(
        "Iterations:",
        result["iteration"],
    )

    print("\n" + "=" * 70)
    print("VALIDATION ERRORS")
    print("=" * 70)

    for error in result["validation_errors"]:

        print(error)

    print("\n" + "=" * 70)
    print("RETRIEVED SOURCES")
    print("=" * 70)

    for source in result["sources"]:

        print(source)


if __name__ == "__main__":
    main()
from app.rag.bm25_index import build_bm25_index
from app.rag.bm25_service import get_bm25_service


def main():
    file_path = (
        "data/documents/"
        "sap_naming_rules/"
        "demo_sap_naming_rules.txt"
    )

    count = build_bm25_index(
        file_path=file_path,
        category="sap_naming_rules",
    )

    print("BM25 documents indexed:", count)

    service = get_bm25_service()

    query = "LT_ internal table"

    results = service.search(
        query=query,
        top_k=3,
    )

    print("\nQUERY:")
    print(query)

    print("\nRESULTS:")

    for index, result in enumerate(results, start=1):
        print("\n" + "=" * 60)
        print(f"RESULT {index}")
        print("=" * 60)

        print("Score:", result["score"])

        print("\nText:")
        print(result["text"])

        print("\nMetadata:")
        print(result["metadata"])


if __name__ == "__main__":
    main()
from app.rag.retriever import retrieve_documents


def main():
    query = (
        "What prefix should I use for "
        "a local internal table?"
    )

    results = retrieve_documents(
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
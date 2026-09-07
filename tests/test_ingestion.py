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

    print("\nNumber of chunks:", len(chunks))

    for index, chunk in enumerate(chunks):
        print("\n" + "=" * 60)
        print(f"CHUNK {index}")
        print("=" * 60)

        print("CONTENT:")
        print(chunk.page_content)

        print("\nMETADATA:")
        print(chunk.metadata)


if __name__ == "__main__":
    main()
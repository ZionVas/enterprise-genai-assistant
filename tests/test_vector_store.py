from app.ingestion.pipeline import ingest_document
from app.rag.vector_store import store_documents


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

    count = store_documents(chunks)

    print("Documents stored:", count)


if __name__ == "__main__":
    main()
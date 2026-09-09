from app.rag.embedding_service import get_embedding_service


def main():
    embedding_service = get_embedding_service()

    text = "Local internal tables should begin with LT_."

    embedding = embedding_service.embed_query(text)

    print("Embedding dimension:", len(embedding))
    print("First five values:", embedding[:5])


if __name__ == "__main__":
    main()
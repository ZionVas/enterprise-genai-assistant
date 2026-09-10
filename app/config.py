import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # -----------------------------
    # LLM Configuration
    # -----------------------------
    LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:4b")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    # -----------------------------
    # Qdrant Configuration
    # -----------------------------
    QDRANT_URL = os.getenv(
        "QDRANT_URL",
        "http://localhost:6333",
    )

    # -----------------------------
    # Embedding Configuration
    # -----------------------------
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "BAAI/bge-m3",
    )

    # -----------------------------
    # Reranker Configuration
    # -----------------------------
    RERANKER_MODEL = os.getenv(
        "RERANKER_MODEL",
        "BAAI/bge-reranker-v2-m3",
    )

    # -----------------------------
    # Retrieval Configuration
    # -----------------------------
    RETRIEVAL_K = int(
        os.getenv("RETRIEVAL_K", "10")
    )

    TOP_K = int(
        os.getenv("TOP_K", "5")
    )

    RRF_K = int(
        os.getenv("RRF_K", "60")
    )

    # -----------------------------
    # SAP Optimization
    # -----------------------------
    MAX_OPTIMIZATION_ITERATIONS = int(
        os.getenv(
            "MAX_OPTIMIZATION_ITERATIONS",
            "2",
        )
    )
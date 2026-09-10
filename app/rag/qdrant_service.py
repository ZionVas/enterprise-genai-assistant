from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import Config


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=Config.QDRANT_URL
        )

    def create_collection(
        self,
        collection_name: str,
        vector_size: int,
    ):
        collections = self.client.get_collections()

        existing_names = {
            collection.name
            for collection in collections.collections
        }

        if collection_name in existing_names:
            return

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def collection_exists(
        self,
        collection_name: str,
    ) -> bool:
        collections = self.client.get_collections()

        return collection_name in {
            collection.name
            for collection in collections.collections
        }


_qdrant_service = None


def get_qdrant_service() -> QdrantService:
    global _qdrant_service

    if _qdrant_service is None:
        _qdrant_service = QdrantService()

    return _qdrant_service
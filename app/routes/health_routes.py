from flask import Blueprint, jsonify

from app.rag.qdrant_service import get_qdrant_service


health_bp = Blueprint(
    "health",
    __name__,
)


@health_bp.get("/health")
def health_check():

    try:
        qdrant = get_qdrant_service()

        qdrant.client.get_collections()

        return jsonify(
            {
                "status": "ok",
                "qdrant": "ok",
            }
        )

    except Exception as exc:

        return jsonify(
            {
                "status": "error",
                "qdrant": "unavailable",
                "error": str(exc),
            }
        ), 503
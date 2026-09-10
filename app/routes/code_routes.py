from flask import Blueprint, jsonify, request

from app.services.code_generation_graph import (
    build_code_generation_graph,
)


code_bp = Blueprint(
    "code",
    __name__,
)


@code_bp.route(
    "/api/generate-code",
    methods=["POST"],
)
def generate_code():

    data = request.get_json()

    if not data:
        return jsonify(
            {
                "error": "Request body is required."
            }
        ), 400

    user_request = data.get(
        "user_request",
        "",
    ).strip()

    language = data.get(
        "language",
        "Python",
    ).strip()

    if not user_request:
        return jsonify(
            {
                "error": "user_request is required."
            }
        ), 400

    try:
        graph = build_code_generation_graph()

        result = graph.invoke(
            {
                "user_request": user_request,
                "language": language,
                "retrieved_context": "",
                "sources": [],
                "response": "",
            }
        )

        return jsonify(
            {
                "success": True,
                "generated_code": result["response"],
                "sources": result["sources"],
            }
        )

    except Exception as error:

        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500
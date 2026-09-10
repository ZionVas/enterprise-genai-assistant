from flask import Blueprint, jsonify, render_template, request

from app.services.sap_optimization_graph import (
    build_sap_optimization_graph,
)


sap_optimization_bp = Blueprint(
    "sap_optimization",
    __name__,
)


@sap_optimization_bp.route(
    "/sap-optimization",
    methods=["GET"],
)
def sap_optimization_page():

    return render_template(
        "sap_optimization.html"
    )


@sap_optimization_bp.route(
    "/api/sap-optimization",
    methods=["POST"],
)
def optimize_sap_code():

    data = request.get_json()

    if not data:
        return jsonify(
            {
                "success": False,
                "error": "Request body is required.",
            }
        ), 400

    original_code = data.get(
        "original_code",
        "",
    ).strip()

    if not original_code:
        return jsonify(
            {
                "success": False,
                "error": "SAP ABAP code is required.",
            }
        ), 400

    try:

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

        return jsonify(
            {
                "success": True,
                "original_code": original_code,
                "optimized_code": result[
                    "optimized_code"
                ],
                "validation_passed": result[
                    "validation_passed"
                ],
                "validation_errors": result[
                    "validation_errors"
                ],
                "iterations": result[
                    "iteration"
                ],
                "sources": result[
                    "sources"
                ],
            }
        )

    except Exception as error:

        print(
            f"SAP optimization error: {error}"
        )

        return jsonify(
            {
                "success": False,
                "error": (
                    "An error occurred while "
                    "optimizing the SAP ABAP code."
                ),
            }
        ), 500
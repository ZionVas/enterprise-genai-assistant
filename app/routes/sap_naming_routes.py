from flask import Blueprint, jsonify, render_template, request

from app.services.sap_naming_graph import (
    build_sap_naming_graph,
)


sap_naming_bp = Blueprint(
    "sap_naming",
    __name__,
)


@sap_naming_bp.route(
    "/sap-naming",
    methods=["GET"],
)
def sap_naming_page():

    return render_template(
        "sap_naming.html"
    )


@sap_naming_bp.route(
    "/api/sap-naming",
    methods=["POST"],
)
def correct_sap_naming():

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

        graph = build_sap_naming_graph()

        result = graph.invoke(
            {
                "original_code": original_code,
                "retrieved_context": "",
                "sources": [],
                "corrected_code": "",
            }
        )

        return jsonify(
            {
                "success": True,
                "original_code": original_code,
                "corrected_code": result[
                    "corrected_code"
                ],
                "sources": result["sources"],
            }
        )

    except Exception as error:

        print(
            f"SAP naming correction error: {error}"
        )

        return jsonify(
            {
                "success": False,
                "error": (
            "An error occurred while "
            "processing the SAP ABAP code."
                ),
            }
        ), 500
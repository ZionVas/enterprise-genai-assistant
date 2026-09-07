from flask import Blueprint, render_template, request, jsonify

from app.services.generation_graph import build_generation_graph

from app.services.email_graph import build_email_graph


main_bp = Blueprint("main", __name__)

generation_graph = build_generation_graph()

email_graph = build_email_graph()


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/text")
def text_generation():
    return render_template("text.html")


@main_bp.route("/email")
def email_generation():
    return render_template("email.html")


@main_bp.route("/code")
def code_generation():
    return render_template("code.html")


@main_bp.route("/sap/naming")
def sap_naming():
    return render_template("sap_naming.html")


@main_bp.route("/sap/optimization")
def sap_optimization():
    return render_template("sap_optimization.html")


@main_bp.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()

    user_input = data.get("prompt", "").strip()

    if not user_input:
        return jsonify({
            "success": False,
            "error": "Prompt cannot be empty."
        }), 400

    try:
        result = generation_graph.invoke({
            "user_input": user_input,
            "response": ""
        })

        return jsonify({
            "success": True,
            "response": result["response"]
        })

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 500

@main_bp.route("/api/generate-email", methods=["POST"])
def generate_email():

    data = request.get_json()

    recipient = data.get("recipient", "").strip()
    purpose = data.get("purpose", "").strip()
    key_points = data.get("key_points", "").strip()
    tone = data.get("tone", "professional").strip()
    length = data.get("length", "medium").strip()

    if not purpose:
        return jsonify({
            "success": False,
            "error": "Email purpose cannot be empty."
        }), 400

    try:

        result = email_graph.invoke(
            {
                "recipient": recipient,
                "purpose": purpose,
                "key_points": key_points,
                "tone": tone,
                "length": length,
                "response": "",
            }
        )

        return jsonify({
            "success": True,
            "response": result["response"]
        })

    except Exception as exc:

        return jsonify({
            "success": False,
            "error": str(exc)
        }), 500    
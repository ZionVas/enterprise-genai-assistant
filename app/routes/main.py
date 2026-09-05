from flask import Blueprint, render_template


main_bp = Blueprint("main", __name__)


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
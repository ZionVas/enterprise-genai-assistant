from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Enterprise GenAI Assistant is running!"

    return app
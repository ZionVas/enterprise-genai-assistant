from flask import Flask


def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    from app.routes.main import main_bp

    app.register_blueprint(main_bp)

    return app
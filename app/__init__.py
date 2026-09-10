from flask import Flask
from app.routes.code_routes import code_bp
from app.routes.sap_naming_routes import sap_naming_bp
from app.routes.sap_optimization_routes import sap_optimization_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    from app.routes.main import main_bp

    app.register_blueprint(main_bp)

    app.register_blueprint(code_bp)

    app.register_blueprint(sap_naming_bp)

    app.register_blueprint(sap_optimization_bp)

    return app
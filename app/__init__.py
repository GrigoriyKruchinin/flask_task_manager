from flask import Flask, json, jsonify
from config import Config
from .docs import get_apispec, swagger_ui_blueprint
from .db import db, migrate
from .docs import SWAGGER_URL
from dotenv import load_dotenv
from apispec.exceptions import APISpecError

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes

    app.register_blueprint(routes.bp)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/swagger.json")
    def create_swagger_spec():
        return json.dumps(get_apispec(app).to_dict())

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, APISpecError):
            return jsonify({"error": str(e)}), 400
        else:
            return jsonify({"error": "Internal server error"}), 500

    return app

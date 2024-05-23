from flask import Flask, json, jsonify
from config import Config
from .docs import get_apispec, swagger_ui_blueprint
from .db import db, migrate
from .docs import SWAGGER_URL
from dotenv import load_dotenv
from apispec.exceptions import APISpecError

load_dotenv()


def create_app():
    """
    Создание экземпляра приложения Flask.

    Returns:
        app: Экземпляр приложения Flask.
    """
    app = Flask(__name__)  # Создание экземпляра приложения Flask
    app.config.from_object(Config)  # Применение конфигурации к приложению

    db.init_app(app)  # Инициализация базы данных для приложения
    migrate.init_app(app, db)  # Инициализация миграций для базы данных

    from . import routes  # Импорт маршрутов приложения

    app.register_blueprint(routes.bp)  # Регистрация маршрутов в приложении
    app.register_blueprint(
        swagger_ui_blueprint, url_prefix=SWAGGER_URL
    )  # Регистрация Swagger UI в приложении

    @app.route("/swagger.json")
    def create_swagger_spec():
        """
        Создание спецификации API в формате JSON.

        Returns:
            str: Спецификация API в формате JSON.
        """
        return json.dumps(
            get_apispec(app).to_dict()
        )  # Возврат спецификации API в формате JSON

    @app.errorhandler(Exception)
    def handle_exception(e):
        """
        Обработчик исключений для обработки ошибок.

        Args:
            e: Исключение, которое необходимо обработать.

        Returns:
            response: Ответ с информацией об ошибке.
        """
        if isinstance(e, APISpecError):  # Если возникло исключение APISpecError
            return (
                jsonify({"error": str(e)}),
                400,
            )  # Возврат сообщения об ошибке валидации данных, код ошибки 400
        else:  # В противном случае
            return (
                jsonify({"error": "Internal server error"}),
                500,
            )  # Возврат сообщения об ошибке сервера, код ошибки 500

    return app  # Возврат экземпляра приложения Flask

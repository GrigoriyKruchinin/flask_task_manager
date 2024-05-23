from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint

from app.schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema

# Определение URL для Swagger UI
SWAGGER_URL = "/docs"
API_URL = "/swagger.json"

# Создание blueprint для Swagger UI
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Task API"}
)

# Функция для создания тегов в спецификации Swagger
def create_tags(spec):
    tags = [{"name": "Task manager", "description": "Управление задачами"}]
    for tag in tags:
        spec.tag(tag)

# Функция для получения экземпляра APISpec
def get_apispec(app):
    spec = APISpec(
        title="Task manager API",
        version="1.0.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    # Добавление схем в компоненты спецификации
    spec.components.schema("TaskSchema", schema=TaskSchema)
    spec.components.schema("TaskCreateSchema", schema=TaskCreateSchema)
    spec.components.schema("TaskUpdateSchema", schema=TaskUpdateSchema)

    # Создание тегов
    create_tags(spec)

    # Загрузка документации из docstrings
    load_docstrings(spec, app)

    return spec

# Функция для загрузки документации из docstrings
def load_docstrings(spec, app):
    for fn_name in app.view_functions:
        if fn_name == "static":
            continue
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)

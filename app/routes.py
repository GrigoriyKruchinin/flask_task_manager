from flask import Blueprint, request, jsonify
from . import db
from .models import Task
from .schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=["POST"])
def create_task():
    """
    ---
    post:
      summary: Создать новую задачу
      requestBody:
        required: true
        content:
          application/json:
            schema: TaskCreateSchema
      responses:
        '201':
          description: Задача успешно создана
          content:
            application/json:
              schema: TaskSchema
        '400':
          description: Ошибка валидации
    """
    schema = TaskCreateSchema()
    task_data = schema.load(request.get_json())
    task = Task(**task_data)
    db.session.add(task)
    db.session.commit()
    return schema.dump(task), 201


@bp.route("", methods=["GET"])
def get_tasks():
    """
    ---
    get:
      summary: Получить список задач
      responses:
        '200':
          description: Успешный ответ
          content:
            application/json:
              schema:
                type: array
                items: TaskSchema
    """
    tasks = Task.query.all()
    schema = TaskSchema(many=True)
    return schema.dump(tasks), 200


@bp.route("/<int:id>", methods=["GET"])
def get_task(id):
    """
    ---
    get:
      summary: Получить задачу по ID
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Успешный ответ
          content:
            application/json:
              schema: TaskSchema
        '404':
          description: Задача не найдена
    """
    task = Task.query.get_or_404(id)
    schema = TaskSchema()
    return schema.dump(task), 200


@bp.route("/<int:id>", methods=["PUT"])
def update_task(id):
    """
    ---
    put:
      summary: Обновить существующую задачу
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: TaskUpdateSchema
      responses:
        '200':
          description: Задача успешно обновлена
          content:
            application/json:
              schema: TaskSchema
        '400':
          description: Ошибка валидации
        '404':
          description: Задача не найдена
    """
    task = Task.query.get_or_404(id)
    schema = TaskUpdateSchema()
    updated_data = schema.load(request.get_json(), partial=True)
    for key, value in updated_data.items():
        setattr(task, key, value)
    db.session.commit()
    return schema.dump(task), 200


@bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    """
    ---
    delete:
      summary: Удалить задачу по ID
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Задача успешно удалена
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Task deleted successfully"
        '404':
          description: Задача не найдена
    """
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200


def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }

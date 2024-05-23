from flask import Blueprint, request, jsonify
from . import db
from .models import Task
from .schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema

# Создание Blueprint для управления задачами
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
            schema: TaskCreateSchema  # Схема для валидации данных при создании задачи
      responses:
        '201':
          description: Задача успешно создана
          content:
            application/json:
              schema: TaskSchema  # Схема для возвращаемых данных о задаче
        '400':
          description: Ошибка валидации
    """
    schema = TaskCreateSchema()  # Создание схемы для валидации данных
    task_data = schema.load(request.get_json())  # Загрузка данных из запроса
    task = Task(**task_data)  # Создание новой задачи
    db.session.add(task)  # Добавление задачи в сессию базы данных
    db.session.commit()  # Фиксация изменений в базе данных
    output_schema = TaskSchema()  # Создание схемы для возвращаемых данных
    return output_schema.dump(task), 201  # Возврат данных о созданной задаче


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
                items: TaskSchema  # Схема для возвращаемого списка задач
    """
    tasks = Task.query.all()  # Получение всех задач из базы данных
    schema = TaskSchema(many=True)  # Создание схемы для сериализации списка задач
    return schema.dump(tasks), 200  # Возврат списка задач в формате JSON


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
              schema: TaskSchema  # Схема для возвращаемых данных о задаче
        '404':
          description: Задача не найдена
    """
    # Получение задачи из базы данных или возврат ошибки 404, если задача не найдена
    task = Task.query.get_or_404(id)
    schema = TaskSchema()  # Создание схемы для сериализации задачи
    return schema.dump(task), 200  # Возврат данных о задаче в формате JSON


@bp.route("/<int:id>", methods=["PUT"])  # Роут для обновления задачи по ID
def update_task(id):
    """
    ---
    put:
      summary: Обновить существующую задачу  # Описание метода и его назначения
      parameters:  # Описание параметров запроса
        - in: path  # Входные данные из URL
          name: id  # Название параметра
          required: true  # Параметр обязателен
          schema:
            type: integer  # Тип параметра - целое число
      requestBody:  # Тело запроса
        required: true  # Тело запроса обязательно
        content:
          application/json:
            schema: TaskUpdateSchema  # Схема для валидации данных при обновлении задачи
      responses:  # Описание возможных ответов сервера
        '200':
          description: Задача успешно обновлена  # Описание успешного ответа
          content:
            application/json:
              schema: TaskSchema  # Схема для возвращаемых данных о задаче после обновления
        '400':
          description: Ошибка валидации  # Описание ошибки при валидации данных
        '404':
          description: Задача не найдена  # Описание ошибки, если задача не найдена
    """
    # Получение задачи из базы данных или возврат ошибки 404, если задача не найдена
    task = Task.query.get_or_404(id)
    schema = TaskUpdateSchema()  # Создание схемы для валидации данных
    updated_data = schema.load(
        request.get_json(), partial=True
    )  # Загрузка данных из запроса
    for key, value in updated_data.items():
        setattr(task, key, value)  # Обновление атрибутов задачи
    db.session.commit()  # Фиксация изменений в базе данных
    output_schema = TaskSchema()  # Создание схемы для возвращаемых данных
    return output_schema.dump(task), 200  # Возврат данных о задаче в формате JSON


@bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    """
    ---
    delete:
      summary: Удалить задачу по ID  # Описание метода и его назначения
      parameters:  # Описание параметров запроса
        - in: path  # Входные данные из URL
          name: id  # Название параметра
          required: true  # Параметр обязателен
          schema:
            type: integer  # Тип параметра - целое число
      responses:  # Описание возможных ответов сервера
        '200':
          description: Задача успешно удалена  # Описание успешного ответа
          content:
            application/json:
              schema:
                type: object  # Тип возвращаемого объекта
                properties:
                  message:
                    type: string  # Тип свойства - строка
                    example: "Task deleted successfully"  # Пример сообщения об успешном удалении задачи
        '404':
          description: Задача не найдена  # Описание ошибки, если задача не найдена
    """
    task = Task.query.get_or_404(
        id
    )  # Получение задачи из базы данных или возврат ошибки 404, если задача не найдена
    db.session.delete(task)  # Удаление задачи из сессии базы данных
    db.session.commit()  # Фиксация изменений в базе данных
    return (
        jsonify({"message": "Task deleted successfully"}),
        200,
    )  # Возврат сообщения об успешном удалении задачи


def task_to_dict(task):
    """
    Функция для преобразования объекта задачи в словарь.

    Args:
        task: Объект задачи.

    Returns:
        Словарь с данными о задаче.
    """
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }  # Возврат словаря с данными о задаче

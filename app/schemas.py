from marshmallow import Schema, fields, post_load
from .models import Task


class TaskSchema(Schema):
    # Схема для сериализации и десериализации данных существующей задачи
    id = fields.Int(dump_only=True)  # Поле id только для чтения при сериализации
    title = fields.Str(required=True)  # Обязательное поле названия задачи
    description = fields.Str()  # Поле описания задачи
    created_at = fields.DateTime(
        dump_only=True
    )  # Поле времени создания, только для чтения
    updated_at = fields.DateTime(
        dump_only=True
    )  # Поле времени обновления, только для чтения

    @post_load
    def make_task(self, data, **kwargs):
        # Метод для создания объекта модели Task после десериализации данных
        return Task(**data)


class TaskCreateSchema(Schema):
    # Схема для десериализации данных новой задачи
    title = fields.Str(
        required=True, description="Название задачи", example="Сделать покупки"
    )  # Обязательное поле названия задачи с описанием и примером
    description = fields.Str(
        description="Описание задачи", example="Купить продукты в супермаркете"
    )  # Поле описания задачи с описанием и примером


class TaskUpdateSchema(Schema):
    # Схема для десериализации данных обновления существующей задачи
    title = fields.Str(
        description="Новое название задачи"
    )  # Поле для нового названия задачи
    description = fields.Str(
        description="Новое описание задачи"
    )  # Поле для нового описания задачи

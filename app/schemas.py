from marshmallow import Schema, fields, post_load
from datetime import datetime, timezone
from .models import Task


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)


class TaskCreateSchema(Schema):
    title = fields.Str(
        required=True, description="Название задачи", example="Сделать покупки"
    )
    description = fields.Str(
        description="Описание задачи", example="Купить продукты в супермаркете"
    )


class TaskUpdateSchema(Schema):
    title = fields.Str(description="Новое название задачи")
    description = fields.Str(description="Новое описание задачи")

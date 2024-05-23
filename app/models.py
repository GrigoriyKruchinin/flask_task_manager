from .db import db
from datetime import datetime, timezone


class Task(db.Model):
    # Модель для таблицы задач в базе данных
    id = db.Column(db.Integer, primary_key=True)  # Поле id задачи
    title = db.Column(
        db.String(128), nullable=False
    )  # Поле названия задачи, не может быть пустым
    description = db.Column(db.String(256))  # Поле описания задачи
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # Поле времени создания задачи, по умолчанию текущее время в формате UTC
    updated_at = db.Column(
        db.DateTime,
        default=None,  # Поле времени обновления задачи, изначально None
        onupdate=lambda: datetime.now(
            timezone.utc
        ),  # При обновлении устанавливается текущее время в формате UTC
    )

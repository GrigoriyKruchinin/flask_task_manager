from flask import Blueprint, request, jsonify, abort
from . import db
from .models import Task

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or not "title" in data:
        abort(400, "Title is required")

    task = Task(title=data["title"], description=data.get("description"))
    db.session.add(task)
    db.session.commit()

    return jsonify(task_to_dict(task)), 201


@bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task_to_dict(task) for task in tasks])


@bp.route("/<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task_to_dict(task))


@bp.route("/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]

    db.session.commit()
    return jsonify(task_to_dict(task))


@bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})


def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }

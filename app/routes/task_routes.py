from flask import Blueprint, request, Response, abort, make_response
from .route_utilities import validate_model, create_model, get_all_models
from app.db import db
from app.models.task import Task

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model(Task, request_body)


@bp.get("")
def get_all_tasks():
    return get_all_models(Task)


@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body.get("completed_at")
    except KeyError as e:
        response = {"details": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

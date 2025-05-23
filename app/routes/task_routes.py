from datetime import datetime, timezone
from flask import Blueprint, request, Response, abort, make_response
from .route_utilities import validate_model, create_model, get_all_models
from app.db import db
from app.models.task import Task
import os
import requests

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@bp.post("", strict_slashes=False)
def create_task():
    request_body = request.get_json()

    return create_model(Task, request_body)


@bp.get("", strict_slashes=False)
def get_all_tasks():
    return get_all_models(Task)


@bp.get("/<task_id>", strict_slashes=False)
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}


@bp.put("/<task_id>", strict_slashes=False)
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


@bp.patch("/<task_id>/mark_complete", strict_slashes=False)
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now(tz=timezone.utc)
    db.session.commit()

    api_token = os.environ.get("SLACKBOT_API_KEY")
    channel_id = os.environ.get("SLACK_CHANNEL_ID")
    url = "https://slack.com/api/chat.postMessage"
    body = {
        "channel": f"{channel_id}",
        "text": f"Someone just completed the task {task.title} :kirby_dance:",
        }
    headers = {"Authorization": f"Bearer {api_token}"}

    requests.post(url, json=body, headers=headers)

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete", strict_slashes=False)
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<task_id>", strict_slashes=False)
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

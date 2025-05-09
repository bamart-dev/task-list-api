from flask import Blueprint, request, Response, abort, make_response
from .route_utilities import validate_model, create_model, get_all_models
from app.db import db
from app.models.goal import Goal
from app.models.task import Task

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@bp.post("", strict_slashes=False)
def create_goal():
    request_body = request.get_json()

    return create_model(Goal, request_body)


@bp.post("/<goal_id>/tasks", strict_slashes=False)
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_ids = request.get_json()["task_ids"]
    task_list = []

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal_id
        task_list.append(task)

    goal.tasks = task_list
    db.session.commit()

    return {"id": goal.id, "task_ids": task_ids}


@bp.get("", strict_slashes=False)
def get_all_goals():
    return get_all_models(Goal)


@bp.get("/<goal_id>", strict_slashes=False)
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}


@bp.get("<goal_id>/tasks", strict_slashes=False)
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_tasks = goal.to_dict()

    goal_tasks["tasks"] = [task.to_dict() for task in goal.tasks]

    return goal_tasks


@bp.put("/<goal_id>", strict_slashes=False)
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    try:
        goal.title = request_body["title"]
    except KeyError as e:
        response = {"details": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<goal_id>", strict_slashes=False)
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

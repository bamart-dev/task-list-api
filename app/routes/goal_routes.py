from flask import Blueprint, request, Response, abort, make_response
from .route_utilities import validate_model, create_model, get_all_models
from app.db import db
from app.models.goal import Goal

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model(Goal, request_body)


@bp.get("")
def get_all_goals():
    return get_all_models(Goal)


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}


@bp.put("/<goal_id>")
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


@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

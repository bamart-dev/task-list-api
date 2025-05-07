from sqlalchemy import desc
from flask import abort, make_response, request
from app.db import db


def validate_model(cls, model_id):
    """Check given model ID and return model if ID is valid.

    Returns a model matching the provided ID if ID is an integer and
    a corresponding model exists.
    """
    try:
        model_id = int(model_id)
    except ValueError:
        message = {"error": f"{cls.__name__} ID ({model_id}) not valid."}
        abort(make_response(message, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        message = {"error": f"{cls.__name__} ID ({model_id}) not found."}
        abort(make_response(message, 404))

    return model


def create_model(cls, model_info):
    """Create model from provided dictionary and save in database.

    Creates a model using the contents of a given dictionary, commits
    it to the database, then returns a response. Raises KeyError if
    attributes are missing from request.
    """
    try:
        model = cls.create_from_dict(model_info)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(model)
    db.session.commit()

    return {"task": model.to_dict()}, 201


def get_all_models(cls):
    """Retrieve all models from database."""
    query = db.select(cls)
    order = request.args.get("sort")

    if order == "desc":
        models = db.session.scalars(query.order_by(desc(cls.title)))
    elif order == "asc":
        models = db.session.scalars(query.order_by(cls.title))
    else:
        models = db.session.scalars(query.order_by(cls.id))

    return [model.to_dict() for model in models]

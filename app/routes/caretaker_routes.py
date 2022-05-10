from crypt import methods
from flask import Blueprint, jsonify, abort, make_response, request
from ..models.caretaker import Caretaker
from ..models.cat import Cat
from app import db
from .routes_helper import error_message, get_record_by_id

bp = Blueprint("caretaker", __name__, url_prefix="/caretakers")

@bp.route("", methods=["POST"])
def create_caretaker():
    request_body = request.get_json()
    caretaker = Caretaker.from_dict(request_body)

    db.session.add(caretaker)
    db.session.commit()

    return jsonify(caretaker.to_dict()), 201

@bp.route("", methods=["GET"])
def get_caretakers():
    all_caretakers = Caretaker.query.all()
    caretakers_as_dicts = [caretaker.to_dict() for caretaker in all_caretakers]

    return jsonify(caretakers_as_dicts)

@bp.route("/<caretaker_id>/cats", methods=["POST"])
def create_cat_with_caretaker(caretaker_id):
    caretaker = get_record_by_id(Caretaker, caretaker_id)

    request_body = request.get_json()
    new_cat = Cat.from_dict(request_body)
    new_cat.caretaker = caretaker

    db.session.add(new_cat)
    db.session.commit()

    return jsonify(new_cat.to_dict()), 201

@bp.route("/<caretaker_id>/cats", methods=["GET"])
def get_cats_for_caretaker(caretaker_id):
    caretaker = get_record_by_id(Caretaker, caretaker_id)
    cats_info = [cat.to_dict() for cat in caretaker.cats]

    return jsonify(cats_info)

# def get_caretaker_record_by_id(id):
#     try:
#         id = int(id)
#     except ValueError:
#         error_message(f"Invalid id {id}", 400)

#     caretaker = Caretaker.query.get(id)
#     if caretaker:
#         return caretaker

#     error_message(f"No caretaker with id {id} found", 404)
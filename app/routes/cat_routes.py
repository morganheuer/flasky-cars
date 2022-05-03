from flask import Blueprint, jsonify, abort, make_response, request
from ..models.cat import Cat
from app import db

# class Cat:
#     def __init__(self, id, name, color, personality):
#         self.id = id
#         self.name = name
#         self.color = color
#         self.personality = personality

#     def to_dict(self):
#         return dict(
#             id=self.id,
#             name=self.name,
#             color=self.color,
#             personality=self.personality,
#         )

# cats = [
#     Cat(1, "Muna", "black", "mischevious"),
#     Cat(2, "Matthew", "spotted", "cuddly"),
#     Cat(3, "George", "Gray","Sassy")
# ]

bp = Blueprint("cats", __name__, url_prefix="/cats")

# POST /cats
@bp.route("", methods=("POST",))
def create_cat():
    request_body = request.get_json()

    cat = Cat(
        name=request_body["name"],
        color=request_body["color"],
        personality=request_body["personality"],
        )

    db.session.add(cat)
    db.session.commit()

    return jsonify(cat.to_dict()), 201
    
# GET /cats

@bp.route("", methods=("GET",))
def index_cats():
    cats = Cat.query.all()

    result_list = [cat.to_dict() for cat in cats]

    return jsonify(result_list)

# GET /cats/<cat_id>
@bp.route("/<cat_id>", methods=["GET"])
def get_cat_by_id(cat_id):
    cat = get_cat_record_by_id(cat_id)
    return jsonify(cat.to_dict())

# PUT /cats/<cat_id>
@bp.route("/<cat_id>", methods=["PUT"])
def replace_cat_by_id(cat_id):
    request_body = request.get_json()
    cat = get_cat_record_by_id(cat_id)

    cat.name = request_body["name"]
    cat.personality = request_body["personality"]
    cat.color = request_body["color"]

    db.session.commit()
    return jsonify(cat.to_dict())

# DELETE /cats/<cat_id>
@bp.route("/<cat_id>", methods=["DELETE"])
def delete_cat_by_id(cat_id):
    cat = get_cat_record_by_id(cat_id)
    
    db.session.delete(cat)
    db.session.commit()

    return make_response(f"Cat with id {cat_id} successfully deleted!")

# PATCH /cats/<cat_id>
@bp.route("/<cat_id>", methods=["PATCH"])
def update_cat_with_id(cat_id):
    cat = get_cat_record_by_id(cat_id)
    request_body = request.get_json()
    cat_keys = request_body.keys()

    if "name" in cat_keys:
        cat.name = request_body["name"]
    if "color" in cat_keys:
        cat.color = request_body["color"]
    if "personality" in cat_keys:
        cat.personality = request_body["personality"]

    db.session.commit()
    return jsonify(cat.to_dict())

# Helper function to get a cat from the database
def get_cat_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response(jsonify(dict(details=f"Invalid id {id}")), 400))

    cat = Cat.query.get(id)
    if cat:
        return cat

    abort(make_response(jsonify(dict(details=f"No cat with id {id} found")), 404))

# def validate_cat(id):
#     try:
#         id = int(id)
#     except ValueError:
#         abort(make_response(jsonify(dict(details=f"invalid id: {id}")), 400))

#     for cat in cats:
#         if cat.id == id:
#             # return the cat
#             return cat

#     # no cat found
#     abort(make_response(jsonify(dict(details=f"cat id {id} not found")), 404))    

# # GET /cats/id
# @bp.route("/<id>", methods=("GET",))
# def get_cat(id):
#     cat = validate_cat(id)
#     return jsonify(cat.to_dict())

from flask import Blueprint, jsonify, request, abort, make_response
from app.models.cats import Cat
from app import db

cats_bp = Blueprint('cats_bp', __name__, url_prefix='/cats')

DEBUG = True
def print_debug(data):
    if DEBUG:
        print(data)

@cats_bp.route('', methods=['POST'])
def create_one_cat():
    request_body = request.get_json()
    new_cat = Cat(name=request_body["name"],
                  age=request_body["age"],
                  color=request_body["color"])
    db.session.add(new_cat)
    print_debug(new_cat)
    db.session.commit()
    return {
        "id": new_cat.id,
        "msg": f"Successfully created cat with id {new_cat.id}"
    }, 201

@cats_bp.route('', methods=['GET'])
def get_all_cats():
    params = request.args
    if "color" in params and "age" in params:
        color_name = params["color"]
        age_value = params["age"]
        cats = Cat.query.filter_by(color=color_name, age=age_value)
    elif "color" in params:
        color_name = params["color"]
        cats = Cat.query.filter_by(color=color_name)
    elif "age" in params:
        age_value = params["age"]
        cats = Cat.query.filter_by(age=age_value)
    else:
        cats = Cat.query.all()
        print_debug(cats)
    cats_response = []
    for cat in cats:
        cats_response.append({
            'id': cat.id,
            'name': cat.name,
            'age': cat.age,
            'color': cat.color
        })
    return jsonify(cats_response)


def get_cat_or_abort(cat_id):
    try:
        cat_id = int(cat_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {cat_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_cat = Cat.query.get(cat_id)
    print_debug(chosen_cat)

    if chosen_cat is None:
        rsp = {"msg": f"Could not find cat with id {cat_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_cat
    

@cats_bp.route('/<cat_id>', methods=['GET'])
def get_one_cat(cat_id):
    chosen_cat = get_cat_or_abort(cat_id)
    rsp = {
        'id': chosen_cat.id,
        'name': chosen_cat.name,
        'age': chosen_cat.age,
        'color': chosen_cat.color
    }
    return jsonify(rsp), 200

@cats_bp.route('/<cat_id>', methods=['PUT', 'PATCH'])
def put_one_cat(cat_id):
    chosen_cat = get_cat_or_abort(cat_id)

    request_body = request.get_json()
    try:
        chosen_cat.name = request_body["name"]
        chosen_cat.age = request_body["age"]
        chosen_cat.color = request_body["color"]
    except KeyError:
        return {
            "msg": "name, age, and color are required"
        }, 400
    db.session.commit()

    return {
        "msg": f"cat #{chosen_cat.id} successfully replaced"
    }, 200

@cats_bp.route("/<cat_id>", methods=["DELETE"])
def delete_cat(cat_id):
    chosen_cat = get_cat_or_abort(cat_id)

    db.session.delete(chosen_cat)
    db.session.commit()

    return {
        "msg": f"cat #{chosen_cat.id} successfully destroyed"
    }, 200
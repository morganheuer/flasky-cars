from flask import Blueprint, jsonify, abort, make_response
from ..models.dog import Dog
# class Dog:
#     def __init__(self, id, name, breed, chip):
#         self.id = id
#         self.name = name
#         self.breed = breed
#         self.chip = chip

#     def to_dict(self):
#         return dict(
#             id=self.id,
#             name=self.name,
#             breed=self.breed,
#             chip=self.chip,
#         )

# dogs = [
#     Dog(1, "Fido", "shiba inu", "36wkj6w5jh56j"),
#     Dog(2, "Luna", "corgi", "36wkj6w5jh56j"),
#     Dog(3, "Kuro", "husky","36wkj6w5jh56j"),
#     Dog(4, "Max", "lab","36wkj6w5jh56j")
# ]

bp = Blueprint("dogs", __name__, url_prefix="/dogs")

# GET /dogs

@bp.route("", methods=("GET",))
def index_dogs():
    dogs = Dog.query.all()

    result_list = [dog.to_dict() for dog in dogs]

    return jsonify(result_list)

def get_dog_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response(jsonify(dict(details=f"invalid id: {id}")), 400))

    dog = Dog.query.get(id)
    if dog:
        return dog

    # no dog found
    abort(make_response(jsonify(dict(details=f"dog id {id} not found")), 404))    

# GET /dogs/id
@bp.route("/<id>", methods=("GET",))
def get_dog(id):
    dog = get_dog_record_by_id(id)
    return jsonify(dog.to_dict())

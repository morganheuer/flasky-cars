from flask import Blueprint, jsonify, request, make_response

from app import db
from app.models.cars import Car

cars_bp = Blueprint("cars", __name__, url_prefix="/cars")

@cars_bp.route("", methods=["POST"])
def create_car():
    request_body = request.get_json()

    new_car = Car(
        driver_id=request_body["driver_id"],
        #team=request_body["team"],
        mass_kg=request_body["mass_kg"]
    )

    db.session.add(new_car)
    db.session.commit()

    return {
        "id": new_car.id
    }, 201

@cars_bp.route("", methods=["GET"])
def get_all_cars():
    response = []
    cars = Car.query.all()
    for car in cars:
        response.append(
            car.to_dict()
        )
    return jsonify(response)

@cars_bp.route("/<car_id>", methods=["GET"])
def get_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({'msg': f"Invalid car id: '{car_id}'. ID must be an integer"}), 400

    chosen_car = Car.query.get(car_id)

    if chosen_car is None:
        return jsonify({'msg': f'Could not find car with id {car_id}'}), 404 
            
    return jsonify(chosen_car.to_dict())
    
@cars_bp.route("/<car_id>", methods=["PATCH"])
def update_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({'msg': f"Invalid car id: '{car_id}'. ID must be an integer"}), 400

    request_body = request.get_json()

    if "mass_kg" not in request_body:
       return jsonify({'msg': f"Request must include driver, team, and mass_kg"}), 400

    chosen_car = Car.query.get(car_id)

    if chosen_car is None:
        return jsonify({'msg': f'Could not find car with id {car_id}'}), 404

    chosen_car.mass_kg = request_body["mass_kg"]

    db.session.commit()

    return make_response(
        jsonify({'msg': f"Successfully replaced car with id {car_id}"}),
        200
    )


@cars_bp.route("/<car_id>", methods=["DELETE"])
def delete_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({'msg': f"Invalid car id: '{car_id}'. ID must be an integer"}), 400

    chosen_car = Car.query.get(car_id)

    if chosen_car is None:
        return jsonify({'msg': f'Could not find car with id {car_id}'}), 404

    db.session.delete(chosen_car)
    db.session.commit()

    return jsonify({'msg': f'Deleted car with id {car_id}'})
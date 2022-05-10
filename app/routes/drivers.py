from curses import termname
from unicodedata import name
from flask import Blueprint, jsonify, request, make_response, abort

from app import db
from app.models.drivers import Driver

drivers_bp = Blueprint("drivers", __name__, url_prefix="/drivers")

@drivers_bp.route("", methods=["POST"])
def create_driver():
    request_body = request.get_json()

    new_driver = Driver(
        name=request_body["name"],
        team=request_body["team"],
        country=request_body["country"],
        handsome=request_body["handsome"]
    )

    db.session.add(new_driver)
    db.session.commit()

    return {
        "id": new_driver.id
    }, 201

@drivers_bp.route("", methods=["GET"])
def get_all_drivers():
    response = []
    drivers = Driver.query.all()
    for driver in drivers:
        response.append(
            driver.to_dict()
        )
    return jsonify(response)

def get_one_driver_or_abort(driver_id):
    try:
        driver_id = int(driver_id)
    except ValueError:
        abort(make_response(jsonify({'msg': f"Invalid driver id: '{driver_id}'. ID must be an integer"}), 400))

    chosen_driver = Driver.query.get(driver_id)

    if chosen_driver is None:
        abort(make_response(jsonify({'msg': f'Could not find car with id {driver_id}'}), 404))
    
    return chosen_driver

@drivers_bp.route("/<driver_id>", methods=["GET"])
def get_one_driver(driver_id):
    
    driver = get_one_driver_or_abort(driver_id)
          
    return jsonify(driver.to_dict()), 200
    
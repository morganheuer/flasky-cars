from flask import jsonify, abort, make_response

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

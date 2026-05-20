from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """
    Standardized JSON response for successful operations.
    """
    response = {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(response), status_code

def error_response(message="An error occurred", errors=None, status_code=400):
    """
    Standardized JSON response for error operations.
    """
    response = {
        "success": False,
        "message": message,
        "errors": errors if errors is not None else []
    }
    return jsonify(response), status_code

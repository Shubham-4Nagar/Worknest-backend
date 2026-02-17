from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.services.owner_service import (
    get_owner_spaces_service,
    get_owner_bookings_service,
    get_owner_earnings_service,
    get_owner_dashboard_service
)

# OWNER → Spaces
def get_owner_spaces_controller():
    owner_id = get_jwt_identity()
    result, status = get_owner_spaces_service(owner_id)
    return jsonify(result), status

# OWNER → All bookings
def get_owner_bookings_controller():
    owner_id = get_jwt_identity()
    result, status = get_owner_bookings_service(owner_id)
    return jsonify(result), status

# OWNER → Earnings
def get_owner_earnings_controller():
    owner_id = get_jwt_identity()
    result, status = get_owner_earnings_service(owner_id)
    return jsonify(result), status

# OWNER → Dashboard stats
def get_owner_dashboard_controller():
    owner_id = get_jwt_identity()
    result, status = get_owner_dashboard_service(owner_id)
    return jsonify(result), status

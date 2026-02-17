from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_guard import owner_required
from app.services.booking_service import (
    create_booking_service,
    get_owner_pending_bookings_service,
    update_booking_status_service,
    get_user_bookings_service,
    cancel_booking_service
)
#It handles the REQUEST JWT AND jsonify

# USER → CREATE BOOKING
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    result, status = create_booking_service(user_id, data)
    return jsonify(result), status

# OWNER → View pending bookings
@jwt_required()
@owner_required
def get_owner_pending_bookings():
    owner_id = get_jwt_identity()

    result, status = get_owner_pending_bookings_service(owner_id)
    return jsonify(result), status

# OWNER → Approve / Reject booking
@jwt_required()
@owner_required
def update_booking_status(booking_id):
    owner_id = get_jwt_identity()
    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({"error": "Status is required"}), 400

    result, status = update_booking_status_service(
        owner_id=owner_id,
        booking_id=booking_id,
        status=data["status"]
    )
    return jsonify(result), status

# USER → Get booking history
@jwt_required()
def get_user_bookings_controller():
    user_id = get_jwt_identity()

    result, status = get_user_bookings_service(user_id)
    return jsonify(result), status

# USER → Cancel booking
@jwt_required()
def cancel_booking_controller(booking_id):
    user_id = get_jwt_identity()

    result, status = cancel_booking_service(user_id, booking_id)
    return jsonify(result), status

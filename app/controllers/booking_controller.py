from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_guard import owner_required
from app.services.booking_service import (
    create_booking_service,
    get_owner_pending_bookings_service,
    update_booking_status_service
)
 #USER → CREATE BOOKING
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error":"Invalid JSON body"}), 400

    result, status = create_booking_service(user_id, data)
    return jsonify(result), status

#Owner view pending bookings
@jwt_required()
@owner_required
def get_owner_pending_bookings():
    owner_id = get_jwt_identity()

    result, status = get_owner_pending_bookings_service(owner_id)
    return jsonify(result), status

#owner= approve/reject bookings
@jwt_required()
@owner_required
def update_booking_status(booking_id):
    owner_id = get_jwt_identity()
    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({
            "error":"Status is required"}), 400
    if data["status"] not in ["completed","cancelled"]:
        return jsonify({"error":"Invalid status"}), 400
    
    result, status = update_booking_status_service(
        owner_id=owner_id,
        booking_id=booking_id,
        status=data["status"]
    )

    return jsonify(result), status
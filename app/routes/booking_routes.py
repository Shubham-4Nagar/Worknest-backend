from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.role_guard import owner_required
from app.controllers.booking_controller import (
    create_booking,
    get_owner_pending_bookings,
    update_booking_status
)

booking_bp = Blueprint("bookings",__name__,url_prefix="/bookings")

#User routes
@booking_bp.route("", methods=["POST"])
@jwt_required()
def create():
    return create_booking()

#Owner - View pending bookings 
@booking_bp.route("/owner/pending", methods=["GET"])
@jwt_required()
@owner_required
def owner_booking():
    return get_owner_pending_bookings()

#owner- update the pending status
@booking_bp.route("/owner/<booking_id>", methods=["PATCH"])
@jwt_required()
@owner_required
def owner_update(booking_id):
    return update_booking_status(booking_id)

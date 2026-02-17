from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.role_guard import owner_required
from app.controllers.booking_controller import (
    create_booking,
    get_owner_pending_bookings,
    update_booking_status,
    get_user_bookings_controller,
    cancel_booking_controller
)

booking_bp = Blueprint("bookings", __name__, url_prefix="/bookings")

# USER → CREATE BOOKING
@booking_bp.route("", methods=["POST"])
@jwt_required()
def create():
    return create_booking()


# OWNER → View pending bookings
@booking_bp.route("/owner/pending", methods=["GET"])
@jwt_required()
@owner_required
def owner_booking():
    return get_owner_pending_bookings()


# OWNER → Approve / Reject booking
@booking_bp.route("/owner/<booking_id>", methods=["PATCH"])
@jwt_required()
@owner_required
def owner_update(booking_id):
    return update_booking_status(booking_id)


# USER → Get all bookings of logged-in user
@booking_bp.route("/me", methods=["GET"])
@jwt_required()
def my_bookings():
    return get_user_bookings_controller()


# USER → Cancel own booking
@booking_bp.route("/<booking_id>/cancel", methods=["PATCH"])
@jwt_required()
def cancel_booking(booking_id):
    return cancel_booking_controller(booking_id)

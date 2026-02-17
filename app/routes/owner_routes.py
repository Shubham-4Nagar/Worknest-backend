from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.role_guard import owner_required
from app.controllers.owner_controller import (
    get_owner_spaces_controller,
    get_owner_bookings_controller,
    get_owner_earnings_controller,
    get_owner_dashboard_controller
)
owner_bp = Blueprint("owner", __name__, url_prefix="/owner")

# OWNER → Get all spaces created by owner
@owner_bp.route("/spaces", methods=["GET"])
@jwt_required()
@owner_required
def owner_spaces():
    return get_owner_spaces_controller()

# OWNER → Get all bookings for owner spaces
@owner_bp.route("/bookings", methods=["GET"])
@jwt_required()
@owner_required
def owner_bookings():
    return get_owner_bookings_controller()

# OWNER → Get total earnings
@owner_bp.route("/earnings", methods=["GET"])
@jwt_required()
@owner_required
def owner_earnings():
    return get_owner_earnings_controller()

# OWNER → Dashboard summary
@owner_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@owner_required
def owner_dashboard_stats():
    return get_owner_dashboard_controller()

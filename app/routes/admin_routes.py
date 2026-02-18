# app/routes/admin_routes.py

from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.role_guard import admin_required
from app.controllers.admin_controller import(
    verify_owner,
    get_admin_dashboard,
    get_pending_owners,
    get_all_users,
    get_all_bookings)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/owners/<owner_id>/verify", methods=["PATCH"])
@jwt_required()
@admin_required
def verify_owner_route(owner_id):
    return verify_owner(owner_id)

@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@admin_required
def admin_dashboard_route():
    return get_admin_dashboard()
#Get all the owners/request
@admin_bp.route("/owners/pending", methods=["GET"])
@jwt_required()
@admin_required
def pending_owners_route():
    return get_pending_owners()
#Get all the users
@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def all_users_route():
    return get_all_users()

#Get all the bookings
@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
@admin_required
def all_bookings_route():
    return get_all_bookings()

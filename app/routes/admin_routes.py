# app/routes/admin_routes.py

from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.role_guard import admin_required
from app.controllers.admin_controller import verify_owner

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/owners/<owner_id>/verify", methods=["PATCH"])
@jwt_required()
@admin_required
def verify_owner_route(owner_id):
    return verify_owner(owner_id)

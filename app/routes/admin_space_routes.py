from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.role_guard import admin_required
from app.controllers.admin_space_controller import (
    get_pending_spaces,
    update_space_approval,
    get_all_spaces_admin
)

admin_space_bp = Blueprint("admin_spaces",__name__,url_prefix="/admin/spaces")

@admin_space_bp.route("/pending", methods=["GET"])

@jwt_required()
@admin_required
def pending_spaces():
    return get_pending_spaces()


@admin_space_bp.route("/<space_id>/approval", methods=["PATCH"])
@jwt_required()
@admin_required
def update_approval(space_id):
    return update_space_approval(space_id)

@admin_space_bp.route("", methods=["GET"])
@jwt_required()
@admin_required
def get_all_spaces():
    return get_all_spaces_admin()
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.role_guard import owner_required
from app.controllers.space_controller import (
    create_space_controller,
    list_spaces_controller,
    space_details_controller,
    update_space_controller,
    delete_space_controller
)

space_bp = Blueprint("spaces", __name__, url_prefix="/spaces")

@jwt_required()
@owner_required
@space_bp.route("", methods=["POST"])
def create_space_route():
    return create_space_controller()

#PUBLIC APIs
@space_bp.route("", methods=["GET"])
def list_spaces_route():
    return list_spaces_controller()
#PUBLIC APIs
@space_bp.route("/<space_id>", methods=["GET"])
def space_details_route(space_id):
    return space_details_controller(space_id)

@jwt_required()
@owner_required
@space_bp.route("/<space_id>", methods=["PATCH"])
def update_space_route(space_id):
    return update_space_controller(space_id)

@jwt_required()
@owner_required
@space_bp.route("/<space_id>", methods=["DELETE"])
def delete_space_route(space_id):
    return delete_space_controller(space_id)

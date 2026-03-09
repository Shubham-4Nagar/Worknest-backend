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

#PUBLIC APIs - LIST SPACES
@space_bp.route("", methods=["GET"])
def list_spaces_route():
    return list_spaces_controller()
#DETAILS FOR SPACE
@space_bp.route("/<space_id>", methods=["GET"])
def space_details_route(space_id):
    return space_details_controller(space_id)


#OWNER APIs
#CREATE
@space_bp.route("", methods=["POST"])
@jwt_required()
@owner_required
def create_space_route():
    return create_space_controller()
#UPDATE 
@space_bp.route("/<space_id>", methods=["PATCH"])
@jwt_required()
@owner_required
def update_space_route(space_id):
    return update_space_controller(space_id)
#DELETE
@space_bp.route("/<space_id>", methods=["DELETE"])
@jwt_required()
@owner_required
def delete_space_route(space_id):
    return delete_space_controller(space_id)

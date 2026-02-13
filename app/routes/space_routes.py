from flask import Blueprint
from app.controllers.space_controller import (
    create_space_controller,
    list_spaces_controller,
    space_details_controller,
    update_space_controller,
    delete_space_controller
)

space_bp = Blueprint("spaces", __name__, url_prefix="/spaces")


@space_bp.route("", methods=["POST"])
def create_space_route():
    return create_space_controller()


@space_bp.route("", methods=["GET"])
def list_spaces_route():
    return list_spaces_controller()


@space_bp.route("/<space_id>", methods=["GET"])
def space_details_route(space_id):
    return space_details_controller(space_id)


@space_bp.route("/<space_id>", methods=["PATCH"])
def update_space_route(space_id):
    return update_space_controller(space_id)


@space_bp.route("/<space_id>", methods=["DELETE"])
def delete_space_route(space_id):
    return delete_space_controller(space_id)

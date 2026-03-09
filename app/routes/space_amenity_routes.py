from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.role_guard import owner_required
from app.controllers.space_amenity_controller import (
    add_amenities_to_space_controller,
    get_space_amenities_controller
)

space_amenity_bp = Blueprint("space_amenities",__name__,url_prefix="/spaces")

#add amenities to spaces(Owner)
@space_amenity_bp.route("/<space_id>/amenities", methods=["POST"])
@jwt_required()
@owner_required
def add_amenities(space_id):
    return add_amenities_to_space_controller(space_id)

#Get amenities to space(public)
@space_amenity_bp.route("/<space_id>/amenities", methods=["GET"])
def list_amenities(space_id):
    return get_space_amenities_controller(space_id)

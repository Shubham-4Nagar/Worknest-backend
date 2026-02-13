from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.role_guard import owner_required
from app.controllers.amenity_controller import(
    create_amenity,
    list_amenities
)

amenity_bp = Blueprint("amenities", __name__, url_prefix="/amenities")

#create amenity
@amenity_bp.route("", methods=["POST"])
@jwt_required()
@owner_required
def add_amenity():
    return create_amenity()

#list amenity
@amenity_bp.route("", methods=["GET"])
def list_amenity():
    return list_amenities()
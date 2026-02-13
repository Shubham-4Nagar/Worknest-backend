from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.controllers.wishlist_controller import(
    add_to_wishlist,
    get_user_wishlist,
    remove_from_wishlist
)

wishlist_bp = Blueprint("wishlist", __name__, url_prefix="/wishlist")

#Add to wishlist
@wishlist_bp.route("/<space_id>", methods=["POST"])
@jwt_required()
def add(space_id):
    return add_to_wishlist(space_id)

#Get Wishlist
@wishlist_bp.route("", methods=["GET"])
@jwt_required()
def list_wishlist():
    return get_user_wishlist()

#Remove from wishlist
@wishlist_bp.route("/<space_id>", methods=["DELETE"])
@jwt_required()
def remove(space_id):
    return remove_from_wishlist(space_id)

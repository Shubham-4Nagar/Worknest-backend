from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.wishlist_service import(
    add_to_wishlist_service,
    get_user_wishlist_service,
    remove_from_wishlist_service
)

@jwt_required()
def add_to_wishlist(space_id):
    user_id= get_jwt_identity()

    result, status = add_to_wishlist_service(user_id, space_id)
    return jsonify(result), status

@jwt_required()
def get_user_wishlist():
    user_id= get_jwt_identity()

    result, status = get_user_wishlist_service(user_id)
    return jsonify(result), status

@jwt_required()
def remove_from_wishlist(space_id):
    user_id= get_jwt_identity()

    result, status = remove_from_wishlist_service(user_id,space_id)
    return jsonify(result), status
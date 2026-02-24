from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_guard import owner_required
from app.services.space_service import (
    create_space,
    get_active_spaces,
    get_space_by_id,
    update_space,
    delete_space
)


@jwt_required()
@owner_required
def create_space_controller():

    owner_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        space = create_space(owner_id, data)

        return jsonify({
            "message": "Space created successfully",
            "space_id": str(space.space_id)
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@jwt_required()
@owner_required
def update_space_controller(space_id):

    owner_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        update_space(owner_id, space_id, data)
        return jsonify({"message": "Space updated successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@jwt_required()
@owner_required
def delete_space_controller(space_id):

    owner_id = get_jwt_identity()

    try:
        delete_space(owner_id, space_id)
        return jsonify({"message": "Space deleted successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    
#Public APIs
def list_spaces_controller():
    spaces = get_active_spaces()

    return jsonify([
        {
            "space_id": str(space.space_id),
            "space_name": space.space_name,
            "location": space.location,
            "max_capacity": space.max_capacity,
            "space_type":space.space_type
        }
        for space in spaces
    ]), 200

def space_details_controller(space_id):

    try:
        space = get_space_by_id(space_id)

        return jsonify({
            "space_id": str(space.space_id),
            "space_name": space.space_name,
            "location": space.location,
            "max_capacity": space.max_capacity,
            "space_type":space.space_type,
            "description":space.description,
            "image_url":space.image_url
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


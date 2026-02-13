from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_guard import owner_required
from app.services.space_amenity_service import (
    add_amenities_to_space,
    get_space_amenities)

# OWNER → Add amenities
@jwt_required()
@owner_required
def add_amenities_to_space_controller(space_id):

    owner_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        added_count = add_amenities_to_space(owner_id, space_id, data)

        return jsonify({
            "message": "Amenities added successfully",
            "added_count": added_count
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

# PUBLIC → Get amenities
def get_space_amenities_controller(space_id):

    try:
        amenities = get_space_amenities(space_id)

        return jsonify([
            {
                "amenity_id": str(a.amenity_id),
                "amenity_name": a.amenity_name
            }
            for a in amenities
        ]), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

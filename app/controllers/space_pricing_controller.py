from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_guard import owner_required
from app.services.space_pricing_service import (
    add_space_pricing,
    get_space_pricing,
    delete_space_pricing
)


# Add pricing (Owner only)
@jwt_required()
@owner_required
def add_space_pricing_controller(space_id):

    owner_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        pricing = add_space_pricing(owner_id, space_id, data)

        return jsonify({
            "message": "Space pricing added successfully",
            "pricing_id": str(pricing.pricing_id),
            "space_id": str(pricing.space_id),
            "price_type": pricing.price_type,
            "price_amount": float(pricing.price_amount)
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


# Get pricing for a space (Public)
def get_space_pricing_controller(space_id):

    pricing_list = get_space_pricing(space_id)

    return jsonify([
        {
            "pricing_id": str(p.pricing_id),
            "price_type": p.price_type,
            "price_amount": float(p.price_amount)
        }
        for p in pricing_list
    ]), 200


# Delete pricing (Owner only)
@jwt_required()
@owner_required
def delete_space_pricing_controller(pricing_id):

    owner_id = get_jwt_identity()

    try:
        delete_space_pricing(owner_id, pricing_id)
        return jsonify({
            "message": "Pricing deleted successfully"
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

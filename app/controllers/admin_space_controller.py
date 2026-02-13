from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.role_guard import admin_required
from app.services.admin_space_service import (
    get_pending_spaces_service,
    update_space_approval_service
)

@jwt_required()
@admin_required
def get_pending_spaces():
    result, status = get_pending_spaces_service()
    return jsonify(result), status

@jwt_required()
@admin_required
def update_space_approval(space_id):
    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({"error":"status is required"}), 400
    
    status_value  =data["status"]

    if status_value not in ["active","inactive"]:
        return jsonify({
            "error":"Invalid status value. Allowed: active, inactive"
        }), 400
    
    result, status = update_space_approval_service(space_id, status_value)
    return jsonify(result), status
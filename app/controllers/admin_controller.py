from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_guard import admin_required
from app.services.admin_service import verify_owner_service

@jwt_required()
@admin_required
def admin_dashboard():
    return jsonify({
        "message":"Welcome Admin",
        "status":"Admin access granted"
    }), 200 # OK

@jwt_required()
def verify_owner(owner_id):#Verify owner
    admin_id = get_jwt_identity()
    data = request.get_json()

    result, status = verify_owner_service(owner_id, admin_id, data)
    return jsonify(result), status
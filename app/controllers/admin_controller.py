from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_guard import admin_required
from app.services.admin_service import (
    verify_owner_service,
    get_admin_dashboard_service,
    get_pending_owners_service,
    get_all_users_service,
    get_all_bookings_service
    )

@jwt_required()
@admin_required
def verify_owner(owner_id):#Verify owner
    admin_id = get_jwt_identity()
    data = request.get_json()

    result, status = verify_owner_service(owner_id, admin_id, data)
    return jsonify(result), status

@jwt_required()
@admin_required
def get_admin_dashboard():
    result, status = get_admin_dashboard_service()
    return jsonify(result), status

#Get all pending owners request 
@jwt_required()
@admin_required
def get_pending_owners():
    result, status = get_pending_owners_service()
    return jsonify(result), status

#Get ALL THE USERS
@jwt_required()
@admin_required
def get_all_users():
    result, status = get_all_users_service()
    return jsonify(result), status

#Get all the bookings
@jwt_required()
@admin_required
def get_all_bookings():
    result, status = get_all_bookings_service()
    return jsonify(result), status

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import get_user_notifications_service

@jwt_required()
def get_my_notifications():
    user_id = get_jwt_identity()
    result, status = get_user_notifications_service(user_id)
    return jsonify(result), status

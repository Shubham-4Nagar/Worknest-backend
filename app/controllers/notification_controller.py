from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import(
    get_user_notifications_service,
    mark_all_notifications_read_service,
    mark_notification_read_service
)

@jwt_required()
def get_my_notifications():
    user_id = get_jwt_identity()
    result, status = get_user_notifications_service(user_id)
    return jsonify(result), status

@jwt_required()
def mark_notification_read(notification_id):
    user_id = get_jwt_identity()
    result, status = mark_notification_read_service(user_id, notification_id)
    return jsonify(result), status

@jwt_required()
def mark_all_read():
    user_id = get_jwt_identity()
    result, status = mark_all_notifications_read_service(user_id)
    return jsonify(result), status
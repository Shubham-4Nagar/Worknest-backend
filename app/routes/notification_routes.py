from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.notification_controller import get_my_notifications

notification_bp = Blueprint("notifications", __name__,url_prefix="/notifications")


@notification_bp.route("", methods=["GET"])
@jwt_required()
def list_notification():
    return get_my_notifications()

@notification_bp.route("/<notification_id>/read", methods=["PATCH"])
@jwt_required()
def read_one(notification_id):
    return mark_notification_read(notification_id)

@notification_bp.route("/read-all", methods=["PATCH"])
@jwt_required()
def read_all():
    return mark_all_read()

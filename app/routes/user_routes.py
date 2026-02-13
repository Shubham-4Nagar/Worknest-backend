from flask import Blueprint
from app.controllers.user_controller import register,request_owner

user_bp = Blueprint("users", __name__, url_prefix="/users")

#Register User
@user_bp.route("/register", methods=["POST"])
def register_user():
    return register()

#Request_owner_service
@user_bp.route("/request-owner", methods=["POST"])
def request_owner_route():
    return request_owner()

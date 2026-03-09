from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.user_controller import(
    register,
    request_owner_controller,
    update_my_profile
)

user_bp = Blueprint("users", __name__, url_prefix="/users")

#Register User
@user_bp.route("/register", methods=["POST"])
def register_user():
    return register()

#Request_owner_service
@user_bp.route("/request-owner", methods=["POST"])
@jwt_required()
def request_owner_route():
    return request_owner_controller()

# Update own profile
@user_bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_profile():
    return update_my_profile()

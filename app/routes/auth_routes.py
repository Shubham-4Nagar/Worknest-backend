from flask import Blueprint
from flask import jsonify
from app.controllers.auth_controller import login, me, logout,forgot_password_route,reset_password_route
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.users import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Login User
@auth_bp.route("/login", methods=["POST"])
def login_route():
    return login()

@auth_bp.route("/me", methods=["GET"])
def me_route():
    return me()

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password_api():
    return forgot_password_route()


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password_api():
    return reset_password_route()


@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    return logout()

from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.payment_controller import create_payment

payment_bp = Blueprint("payments",__name__,url_prefix="/payments")

@payment_bp.route("", methods=["POST"])
@jwt_required()
def pay():
    return create_payment()

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.payment_service import create_payment_service

#User - create payment

@jwt_required()
def create_payment():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error":"Invalid JSON body"}), 400

    result, status = create_payment_service(user_id, data)
    return jsonify(result), status


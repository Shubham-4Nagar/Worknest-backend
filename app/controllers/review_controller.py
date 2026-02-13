from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.review_service import(
    create_review_service,
    get_space_reviews_service,
    get_user_reviews_service
)

@jwt_required()
def create_review():
    user_id= get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error":"Invalid JSON body"}), 400

    result, status = create_review_service(user_id, data)
    return jsonify(result), status

def get_space_reviews(space_id):
    result, status = get_space_reviews_service(space_id)
    return jsonify(result), status

@jwt_required()
def get_my_reviews():
    user_id = get_jwt_identity()
    result, status = get_user_reviews_service(user_id)
    return jsonify(result), status

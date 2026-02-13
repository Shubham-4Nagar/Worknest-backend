from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.review_controller import (
    create_review,
    get_space_reviews,
    get_my_reviews
)

review_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

@review_bp.route("", methods=["POST"])
@jwt_required()
def add_review():
    return create_review()

@review_bp.route("/space/<space_id>", methods=["GET"])
def space_reviews(space_id):
    return get_space_reviews(space_id)

@review_bp.route("/me", methods=["GET"])
@jwt_required()
def my_reviews():
    return get_my_reviews()

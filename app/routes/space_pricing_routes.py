from flask import Blueprint
from app.controllers.space_pricing_controller import (
    add_space_pricing_controller,
    get_space_pricing_controller,
    delete_space_pricing_controller
)

space_pricing_bp = Blueprint( "space_pricing",__name__, url_prefix="/spaces")

# Add pricing to a space (Owner only)
@space_pricing_bp.route("/<space_id>/pricing", methods=["POST"])
def add_pricing_route(space_id):
    return add_space_pricing_controller(space_id)


# Get pricing for a space (Public)
@space_pricing_bp.route("/<space_id>/pricing", methods=["GET"])
def get_pricing_route(space_id):
    return get_space_pricing_controller(space_id)


# Delete specific pricing (Owner only)
@space_pricing_bp.route("/pricing/<pricing_id>", methods=["DELETE"])
def delete_pricing_route(pricing_id):
    return delete_space_pricing_controller(pricing_id)

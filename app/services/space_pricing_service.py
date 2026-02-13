from app.extensions import db
from app.models.space_pricing import SpacePricing
from app.models.spaces import Space
from sqlalchemy.exc import IntegrityError

ALLOWED_PRICE_TYPES = ["hourly", "daily", "weekly", "monthly"]


def add_space_pricing(owner_id, space_id, data):

    # Required fields
    required_fields = ["price_type", "price_amount"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    price_type = data["price_type"]
    price_amount = data["price_amount"]

    # ENUM validation
    if price_type not in ALLOWED_PRICE_TYPES:
        raise ValueError(
            f"Invalid price_type. Allowed values: {ALLOWED_PRICE_TYPES}"
        )

    # amount validation
    try:
        price_amount = float(price_amount)
    except (ValueError, TypeError):
        raise ValueError("price_amount must be a number")

    if price_amount <= 0:
        raise ValueError("price_amount must be greater than 0")

    # Ownership + space existence check
    space = Space.query.filter_by(
        space_id=space_id,
        owner_id=owner_id,
        is_active=True
    ).first()

    if not space:
        raise ValueError("Space not found or unauthorized")

    pricing = SpacePricing(
        space_id=space_id,
        price_type=price_type,
        price_amount=price_amount
    )

    try:
        db.session.add(pricing)
        db.session.commit()
        return pricing

    except IntegrityError:
        db.session.rollback()
        raise ValueError(
            "Pricing for this price_type already exists for this space"
        )

    except Exception:
        db.session.rollback()
        raise RuntimeError("Internal server error")

# Get Pricing for a Space (Public)
def get_space_pricing(space_id):

    return SpacePricing.query.filter_by(
        space_id=space_id
    ).all()


# Delete Pricing (Owner only)
def delete_space_pricing(owner_id, pricing_id):

    pricing = SpacePricing.query.join(Space).filter(
        SpacePricing.pricing_id == pricing_id,
        Space.owner_id == owner_id
    ).first()

    if not pricing:
        raise ValueError("Pricing not found or unauthorized")

    db.session.delete(pricing)
    db.session.commit()

    return True

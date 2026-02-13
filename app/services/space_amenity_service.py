from app.extensions import db
from app.models.space_amenities import SpaceAmenity
from app.models.amenities import Amenity
from app.models.spaces import Space
from sqlalchemy.exc import IntegrityError


# OWNER → Add amenities to space
def add_amenities_to_space(owner_id, space_id, data):

    if not data or "amenity_ids" not in data:
        raise ValueError("amenity_ids is required")

    amenity_ids = data["amenity_ids"]

    if not isinstance(amenity_ids, list) or not amenity_ids:
        raise ValueError("amenity_ids must be a non-empty list")

    # Check space ownership + active
    space = Space.query.filter_by(
        space_id=space_id,
        owner_id=owner_id,
        is_active=True
    ).first()

    if not space:
        raise ValueError("Space not found or unauthorized")

    # Validate amenities exist
    valid_amenities = Amenity.query.filter(
        Amenity.amenity_id.in_(amenity_ids)
    ).all()

    if len(valid_amenities) != len(set(amenity_ids)):
        raise ValueError("One or more amenities are invalid")

    added = 0

    try:
        for amenity_id in set(amenity_ids):

            # Prevent duplicate
            exists = SpaceAmenity.query.filter_by(
                space_id=space_id,
                amenity_id=amenity_id
            ).first()

            if not exists:
                mapping = SpaceAmenity(
                    space_id=space_id,
                    amenity_id=amenity_id
                )
                db.session.add(mapping)
                added += 1

        db.session.commit()
        return added

    except IntegrityError:
        db.session.rollback()
        raise ValueError(
            "One or more amenities already linked to this space"
        )

    except Exception:
        db.session.rollback()
        raise RuntimeError("Internal server error")

# PUBLIC → Get amenities of a space
def get_space_amenities(space_id):

    space = Space.query.filter_by(
        space_id=space_id,
        is_active=True
    ).first()

    if not space:
        raise ValueError("Space not found")

    amenities = (
        db.session.query(Amenity)
        .join(SpaceAmenity, Amenity.amenity_id == SpaceAmenity.amenity_id)
        .filter(SpaceAmenity.space_id == space_id)
        .all()
    )
    return amenities
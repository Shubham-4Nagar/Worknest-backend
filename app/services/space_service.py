from app.extensions import db
from app.models.spaces import Space
from sqlalchemy.exc import IntegrityError


VALID_SPACE_TYPES = [
    "private_cabin",
    "hot_desk",
    "meeting_room",
    "event_space"
]


# Create Space
def create_space(owner_id, data):

    required_fields = ["space_name",
                        "location",
                        "max_capacity",
                        "space_type"]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    try:
        max_capacity = int(data["max_capacity"])
        if max_capacity <= 0:
            raise ValueError("max_capacity must be greater than 0")
    except (TypeError, ValueError):
        raise ValueError("max_capacity must be an integer")
    
    if data["space_type"] not in VALID_SPACE_TYPES:
        raise ValueError("Invalid space_type")

    new_space = Space(
        owner_id=owner_id,
        space_name=data["space_name"],
        location=data["location"],
        max_capacity=max_capacity,
        space_type=data["space_type"],
        image_url = data.get("image_url"),
        description=data.get("description"),
        is_active=False #admin approval first 
    )

    try:
        db.session.add(new_space)
        db.session.commit()
        return new_space

    except IntegrityError:
        db.session.rollback()
        raise ValueError("Space with this name already exists for this owner")

    except Exception:
        db.session.rollback()
        raise RuntimeError("Internal server error")


# Get all active spaces (public)
def get_active_spaces():
    return Space.query.filter_by(is_active=True).all()


# Get single space details
def get_space_by_id(space_id):

    space = Space.query.filter_by(
        space_id=space_id,
        is_active=True
    ).first()

    if not space:
        raise ValueError("Space not found")

    return space


# Update Space (Owner only)
def update_space(owner_id, space_id, data):

    space = Space.query.filter_by(
        space_id=space_id,
        owner_id=owner_id
    ).first()

    if not space:
        raise ValueError("Space not found or unauthorized")

    if "space_name" in data:
        space.space_name = data["space_name"]

    if "location" in data:
        space.location = data["location"]

    if "max_capacity" in data:
        try:
            max_capacity = int(data["max_capacity"])
            if max_capacity <= 0:
                raise ValueError("max_capacity must be greater than 0")
            space.max_capacity = max_capacity
        except (TypeError, ValueError):
            raise ValueError("max_capacity must be an integer")
    
    if "space_type" in data:
        if data["space_type"] not in VALID_SPACE_TYPES:
            raise ValueError("Invalid space_type")
        space.space_type = data["space_type"]

    if "description" in data:
        space.description = data["description"]

    if "image_url" in data:
        space.image_url = data["image_url"]

    db.session.commit()
    return space


# Soft Delete Space
def delete_space(owner_id, space_id):

    space = Space.query.filter_by(
        space_id=space_id,
        owner_id=owner_id
    ).first()

    if not space:
        raise ValueError("Space not found or unauthorized")

    space.is_active = False
    db.session.commit()

    return True

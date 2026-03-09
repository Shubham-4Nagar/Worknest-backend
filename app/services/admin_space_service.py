from app.extensions import db
from app.models.spaces import Space

ALLOWED_STATUSES = ["active", "inactive"]


def get_pending_spaces_service():
    try:
        spaces = Space.query.filter_by(is_active=False).all()

        result = []

        for space in spaces:
            result.append({
                "space_id": str(space.space_id),
                "space_name": space.space_name,
                "location": space.location,
                "owner_id": str(space.owner_id),
                "is_active": space.is_active,
                "created_at": space.created_at
            })

        return {"pending_spaces": result}, 200

    except Exception:
        return {"error": "Internal server error"}, 500


def update_space_approval_service(space_id, status):

    if status not in ALLOWED_STATUSES:
        return {"error": "Invalid status"}, 400

    space = Space.query.get(space_id)

    if not space:
        return {"error": "Space not found"}, 404

    if status == "active":
        space.is_active = True
    else:
        space.is_active = False

    db.session.commit()

    return {
        "message": f"Space {status} successfully",
        "space_id": str(space.space_id),
        "is_active": space.is_active
    }, 200

def get_all_spaces_service():
    try:
        spaces = Space.query.all()

        result = []

        for space in spaces:
            result.append({
                "space_id": str(space.space_id),
                "space_name": space.space_name,
                "location": space.location,
                "owner_name": f"{space.owner.first_name} {space.owner.last_name}",
                "is_active": space.is_active,
                "created_at": space.created_at
            })

        return {"spaces": result}, 200

    except Exception:
        return {"error": "Internal server error"}, 500
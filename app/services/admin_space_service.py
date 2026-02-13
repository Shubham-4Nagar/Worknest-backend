from app.extensions import db
from app.models.spaces import Space

ALLOWED_STATUSES = ["active", "inactive"]

def get_pending_spaces_service():
    spaces = Space.query.filter_by(approval_status="pending").all()

    result = []
    for space in spaces:
        result.append({
            "space_id": space.space_id,
            "space_name": space.space_name,
            "location": space.location,
            "owner_id": space.owner_id,
            "status": space.approval_status
        })

    return result, 200


def update_space_approval_service(space_id, status):
    status = status.strip().lower()
    if status not in ALLOWED_STATUSES:
        return {
            "error": f"Invalid status. Allowed values: {ALLOWED_STATUSES}"
        }, 400

    space = Space.query.get(space_id)
    if not space:
        return {"error": "Space not found"}, 404

    space.approval_status = status
    db.session.commit()

    return {
        "message": f"Space {status} successfully",
        "space_id": space.space_id,
        "status": space.approval_status
    }, 200

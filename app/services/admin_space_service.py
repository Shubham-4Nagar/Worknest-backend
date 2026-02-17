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
    space = Space.query.get(space_id)
    if not space_id:
        return{"error":"Space not found"}, 404
    
    if status == "active":
        space.is_active = True
    elif status == "inactive":
        space.is_acive = False
    else:
        return{"error":"Invalid status"}, 400
    db.session.commit()

    return{
        "message":f"Space {status} successfully",
        "space_id": str(space.space_id),
        "is_active": space.is_active
    }, 200 

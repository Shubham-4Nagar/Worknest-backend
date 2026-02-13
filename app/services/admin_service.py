from app.extensions import db
from app.models.owner_verification import OwnerVerification
from app.models.users import User
from app.models.roles import Role

def verify_owner_service(owner_id, admin_id, data):
    try:
        # Validate request body
        if not data or "status" not in data:
            return {"error": "status is required"}, 400

        status = data.get("status")

        if status not in ["approved", "rejected"]:
            return {"error": "Status must be approved or rejected"}, 400

        # Fetch owner verification request
        verification = OwnerVerification.query.filter_by(owner_id=owner_id).first()
        if not verification:
            return {"error": "Owner request not found"}, 404

        # Prevent duplicate approval/rejection
        if verification.status != "pending":
            return {"error": "Request already processed"}, 400

        #  Update verification record
        verification.status = status
        verification.verified_by = admin_id

        # Promote user to Owner role if approved
        if status == "approved":
            owner_role = Role.query.filter_by(role_name="Owner").first()
            if not owner_role:
                return {"error": "Owner role not configured"}, 500

            user = User.query.get(owner_id)
            user.role_id = owner_role.role_id

        db.session.commit()

        return {"message": f"Owner request {status}"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": "Internal server error"}, 500

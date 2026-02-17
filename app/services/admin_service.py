from app.extensions import db
from sqlalchemy import func
from app.models.owner_verification import OwnerVerification
from app.models.users import User
from app.models.roles import Role
from app.models.bookings import Booking
from app.models.payments import Payment
from app.models.spaces import Space

def verify_owner_service(owner_id, admin_id, data):
    try:
        # Validate request body
        if not data or "status" not in data:
            return {"error": "status is required"}, 400

        status = data.get("status")

        if status not in ["approved", "rejected"]:
            return {"error": "Status must be approved or rejected"}, 400

        # Fetch owner verification request
        verification = OwnerVerification.query.filter_by(
            owner_id=owner_id,
            status="pending"
            ).first()
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
    
def get_pending_owners_service():
    try:
        pending_requests =OwnerVerification.query.filter_by(status="pending").all()

        result = []

        for request in pending_requests:
            user = User.query.get(request.owner_id)

            result.append({
                "owner_id": str(request.owner_id),
                "name": f"{user.first_name} {user.last_name}" if user else None,
                "email": user.email if user else None,
                "status": request.status,
                "requested_at": request.created_at
            })
        return {"pending_owners": result}, 200
    except Exception:
        return{"error":"Internal server error"}, 500

#Admin dasboard
def get_admin_dashboard_service():
    try:
        # Total Users
        total_users = User.query.count()

        # Total Owners
        owner_role = Role.query.filter_by(role_name="Owner").first()
        total_owners = 0
        if owner_role:
            total_owners = User.query.filter_by(role_id=owner_role.role_id).count()

        # Total Spaces
        total_spaces = Space.query.count()

        # Total Bookings
        total_bookings = Booking.query.count()

        # Total Revenue (successful payments only)
        total_revenue = (
            db.session.query(func.sum(Payment.amount_paid))
            .filter(Payment.payment_status == "success")
            .scalar()
        )

        return {
            "total_users": total_users,
            "total_owners": total_owners,
            "total_spaces": total_spaces,
            "total_bookings": total_bookings,
            "total_revenue": float(total_revenue or 0)
        }, 200

    except Exception:
        return {"error": "Internal server error"}, 500
    
def get_all_users_service():
    try:
        users = User.query.all()

        result = []

        for user in users:
            result.append({
                "user_id": str(user.user_id),
                "name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "role": user.role.role_name,
                "created_at": user.created_at
            })

        return {"users": result}, 200

    except Exception:
        return {"error": "Internal server error"}, 500


def get_all_bookings_service():
    try:
        bookings = Booking.query.all()

        result = []

        for booking in bookings:
            result.append({
                "booking_id": str(booking.booking_id),
                "user_id": str(booking.user_id),
                "space_id": str(booking.space_id),
                "status": booking.status,
                "total_amount": float(booking.total_amount),
                "start_date": booking.start_date,
                "end_date": booking.end_date
            })

        return {"bookings": result}, 200

    except Exception:
        return {"error": "Internal server error"}, 500


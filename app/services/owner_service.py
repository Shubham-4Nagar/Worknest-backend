from app.models.spaces import Space
from app.models.bookings import Booking
from app.models.payments import Payment
from app.extensions import db
from sqlalchemy import func

# OWNER → Get all spaces
def get_owner_spaces_service(owner_id):

    spaces = Space.query.filter_by(owner_id=owner_id).all()

    result = []

    for space in spaces:
        result.append({
            "space_id": str(space.space_id),
            "space_name": space.space_name,
            "location": space.location,
            "max_capacity": space.max_capacity,
            "is_active": space.is_active,
            "created_at": space.created_at
        })

    return {"spaces": result}, 200

# OWNER → Get all bookings (all statuses)
def get_owner_bookings_service(owner_id):

    bookings = (
        Booking.query.join(Space)
        .filter(Space.owner_id == owner_id)
        .all()
    )

    result = []

    for booking in bookings:
        result.append({
            "booking_id": str(booking.booking_id),
            "user_id": str(booking.user_id),
            "space_id": str(booking.space_id),
            "status": booking.status,
            "start_date": booking.start_date,
            "end_date": booking.end_date,
            "total_amount": float(booking.total_amount)
        })

    return {"bookings": result}, 200

# OWNER → Earnings (from successful payments only)
def get_owner_earnings_service(owner_id):

    total = (
        db.session.query(func.sum(Payment.amount_paid))
        .join(Booking, Payment.booking_id == Booking.booking_id)
        .join(Space, Booking.space_id == Space.space_id)
        .filter(
            Space.owner_id == owner_id,
            Payment.payment_status == "success"
        )
        .scalar()
    )

    return {
        "total_earnings": float(total or 0)
    }, 200

# OWNER → Dashboard stats
def get_owner_dashboard_service(owner_id):

    total_spaces = Space.query.filter_by(owner_id=owner_id).count()

    total_bookings = (
        Booking.query.join(Space)
        .filter(Space.owner_id == owner_id)
        .count()
    )

    pending_bookings = (
        Booking.query.join(Space)
        .filter(
            Space.owner_id == owner_id,
            Booking.status == "pending"
        )
        .count()
    )

    completed_bookings = (
        Booking.query.join(Space)
        .filter(
            Space.owner_id == owner_id,
            Booking.status == "completed"
        )
        .count()
    )

    #Add earning
    total_earning =(
        db.session.query(func.sum(Payment.amount_paid))
        .join(Booking, Payment.booking_id == Booking.booking_id)
        .join(Space, Booking.space_id == Space.space_id)
        .filter(
            Space.owner_id == owner_id,
            Payment.payment_status == "success"
        )
        .scalar()
    )

    return {
        "total_spaces": total_spaces,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "completed_bookings": completed_bookings,
        "total_earning": float(total_earning or 0)
    }, 200

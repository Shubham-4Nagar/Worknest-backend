import uuid
from app.models.spaces import Space
from app.models.bookings import Booking
from app.models.payments import Payment
from app.extensions import db
from sqlalchemy import func


def _to_uuid(val):
    """Safely convert JWT identity string to UUID object."""
    try:
        return uuid.UUID(str(val))
    except (ValueError, AttributeError):
        return None


# OWNER → Get all spaces
def get_owner_spaces_service(owner_id):
    uid = _to_uuid(owner_id)
    if not uid:
        return {"spaces": []}, 200

    spaces = Space.query.filter_by(owner_id=uid).all()
    result = []
    for space in spaces:
        result.append({
            "space_id":     str(space.space_id),
            "space_name":   space.space_name,
            "location":     space.location,
            "max_capacity": space.max_capacity,
            "space_type":   space.space_type if hasattr(space, 'space_type') else '',
            "description":  space.description if hasattr(space, 'description') else '',
            "is_active":    space.is_active,
            "status":       "active" if space.is_active else "inactive",
            "created_at":   space.created_at.isoformat() if space.created_at else None,
        })
    return {"spaces": result}, 200


# OWNER → Get ALL bookings for owner spaces (all statuses, full detail)
def get_owner_bookings_service(owner_id):
    uid = _to_uuid(owner_id)
    if not uid:
        return {"bookings": []}, 200

    bookings = (
        Booking.query.join(Space)
        .filter(Space.owner_id == uid)
        .order_by(Booking.created_at.desc())
        .all()
    )
    result = []
    for b in bookings:
        result.append({
            "booking_id":       str(b.booking_id),
            "user_id":          str(b.user_id),
            "user_name":        f"{b.user.first_name} {b.user.last_name}" if b.user else "Unknown",
            "space_id":         str(b.space_id),
            "space_name":       b.space.space_name if b.space else "Unknown",
            "booking_type":     b.booking_type.type_name if b.booking_type else "N/A",
            "status":           b.status,
            "start_date":       b.start_date.isoformat() if b.start_date else None,
            "end_date":         b.end_date.isoformat() if b.end_date else None,
            "number_of_people": b.number_of_people,
            "total_amount":     float(b.total_amount),
        })
    return {"bookings": result}, 200


# OWNER → Earnings (from successful payments only)
def get_owner_earnings_service(owner_id):
    uid = _to_uuid(owner_id)
    if not uid:
        return {"total_earnings": 0}, 200

    total = (
        db.session.query(func.sum(Payment.amount_paid))
        .join(Booking, Payment.booking_id == Booking.booking_id)
        .join(Space, Booking.space_id == Space.space_id)
        .filter(Space.owner_id == uid, Payment.payment_status == "success")
        .scalar()
    )
    return {"total_earnings": float(total or 0)}, 200


# OWNER → Dashboard stats
def get_owner_dashboard_service(owner_id):
    uid = _to_uuid(owner_id)
    if not uid:
        return {"total_spaces": 0, "total_bookings": 0,
                "pending_bookings": 0, "completed_bookings": 0,
                "total_earning": 0}, 200

    total_spaces = Space.query.filter_by(owner_id=uid).count()
    total_bookings = (
        Booking.query.join(Space).filter(Space.owner_id == uid).count()
    )
    pending_bookings = (
        Booking.query.join(Space)
        .filter(Space.owner_id == uid, Booking.status == "pending")
        .count()
    )
    completed_bookings = (
        Booking.query.join(Space)
        .filter(Space.owner_id == uid, Booking.status == "completed")
        .count()
    )
    total_earning = (
        db.session.query(func.sum(Payment.amount_paid))
        .join(Booking, Payment.booking_id == Booking.booking_id)
        .join(Space, Booking.space_id == Space.space_id)
        .filter(Space.owner_id == uid, Payment.payment_status == "success")
        .scalar()
    )
    return {
        "total_spaces":       total_spaces,
        "total_bookings":     total_bookings,
        "pending_bookings":   pending_bookings,
        "completed_bookings": completed_bookings,
        "total_earning":      float(total_earning or 0),
    }, 200

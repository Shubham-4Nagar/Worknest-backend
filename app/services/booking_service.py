import math
import uuid
from decimal import Decimal
from datetime import datetime, timedelta
from app.extensions import db
from app.models.bookings import Booking
from app.models.spaces import Space
from app.models.booking_types import BookingType
from app.models.space_pricing import SpacePricing


# ------------------------------------------------------------------ #
# Helper: normalise incoming date strings robustly
# ------------------------------------------------------------------ #
def _parse_dt(value: str) -> datetime:
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(f"Cannot parse date: {value}")


# ------------------------------------------------------------------ #
# USER → Create booking
# Accepts the rich payload OR the simplified booking_date form used
# by the frontend My-Bookings page.
# ------------------------------------------------------------------ #
def create_booking_service(user_id, data):
    try:
        # JWT identity is always a string — convert to UUID for DB
        uid = uuid.UUID(str(user_id))
    except (ValueError, AttributeError):
        return {"error": "Invalid user identity"}, 401

    try:
        # ---- Normalise simple booking_date into start/end ----
        if "booking_date" in data and "start_date" not in data:
            try:
                base = datetime.fromisoformat(data["booking_date"])
            except ValueError:
                return {"error": "Invalid booking_date format. Use YYYY-MM-DD"}, 400
            data = dict(data)           # don't mutate the original
            data["start_date"] = base.strftime("%Y-%m-%dT09:00:00")
            data["end_date"]   = (base + timedelta(hours=8)).strftime("%Y-%m-%dT17:00:00")

        # ---- Required fields ----
        required_fields = [
            "space_id",
            "start_date",
            "end_date",
        ]
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        # ---- space_id ----
        try:
            space_id = uuid.UUID(data["space_id"])
        except (ValueError, AttributeError):
            return {"error": "Invalid space_id format"}, 400

        # ---- number_of_people (default 1 if missing) ----
        try:
            number_of_people = int(data.get("number_of_people", 1))
        except (ValueError, TypeError):
            return {"error": "number_of_people must be an integer"}, 400

        # ---- Dates ----
        try:
            start_date = _parse_dt(data["start_date"])
            end_date   = _parse_dt(data["end_date"])
        except ValueError as exc:
            return {"error": str(exc)}, 400

        if end_date <= start_date:
            return {"error": "end_date must be after start_date"}, 400

        # ---- Space exists & active ----
        space = Space.query.filter_by(space_id=space_id, is_active=True).first()
        if not space:
            return {"error": "Space not available for booking"}, 404

        # ---- Capacity ----
        if number_of_people > space.max_capacity:
            return {"error": "Exceeds space capacity"}, 400

        # ---- Booking type: use provided or fall back to first available ----
        booking_type_id = data.get("booking_type_id")
        if booking_type_id:
            booking_type = BookingType.query.get(booking_type_id)
            if not booking_type:
                return {"error": "Invalid booking type"}, 400
        else:
            # Pick first pricing option available for this space
            any_pricing = SpacePricing.query.filter_by(space_id=space_id).first()
            if not any_pricing:
                return {"error": "No pricing configured for this space"}, 400
            booking_type = BookingType.query.filter_by(
                type_name=any_pricing.price_type
            ).first()
            if not booking_type:
                # last resort: any booking type
                booking_type = BookingType.query.first()
            if not booking_type:
                return {"error": "No booking types configured in the system"}, 400
            booking_type_id = booking_type.id

        # ---- Pricing ----
        pricing = SpacePricing.query.filter_by(
            space_id=space_id,
            price_type=booking_type.type_name.lower()
        ).first()
        if not pricing:
            # fallback: any pricing for this space
            pricing = SpacePricing.query.filter_by(space_id=space_id).first()
        if not pricing:
            return {"error": "No pricing available for this space"}, 400

        # ---- Overlap check ----
        overlapping = Booking.query.filter(
            Booking.space_id == space_id,
            Booking.status != "cancelled",
            Booking.start_date < end_date,
            Booking.end_date > start_date
        ).first()
        if overlapping:
            return {"error": "Space already booked for this time"}, 409

        # ---- Calculate total ----
        duration_seconds = (end_date - start_date).total_seconds()
        price_per_unit = Decimal(str(pricing.price_amount))

        if booking_type.type_name.lower() == "hourly":
            duration_hours = math.ceil(duration_seconds / 3600)
            total_amount = price_per_unit * Decimal(duration_hours)
        else:
            total_amount = price_per_unit

        # ---- Create booking ----
        booking = Booking(
            user_id=uid,
            space_id=space_id,
            booking_type_id=booking_type_id,
            start_date=start_date,
            end_date=end_date,
            number_of_people=number_of_people,
            total_amount=total_amount,
            status="pending"
        )
        db.session.add(booking)
        db.session.commit()

        return {
            "message": "Booking created, waiting for owner approval",
            "booking_id": str(booking.booking_id),
            "status": booking.status,
            "total_amount": float(total_amount)
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": "Internal server error", "details": str(e)}, 500


# ------------------------------------------------------------------ #
# OWNER → Get all pending bookings
# ------------------------------------------------------------------ #
def get_owner_pending_bookings_service(owner_id):
    try:
        uid = uuid.UUID(str(owner_id))
    except (ValueError, AttributeError):
        return [], 200

    bookings = (
        Booking.query.join(Space, Booking.space_id == Space.space_id)
        .filter(Space.owner_id == uid, Booking.status == "pending")
        .all()
    )
    result = []
    for b in bookings:
        result.append({
            "booking_id":      str(b.booking_id),
            "space_id":        str(b.space_id),
            "space_name":      b.space.space_name,
            "user_id":         str(b.user_id),
            "user_name":       f"{b.user.first_name} {b.user.last_name}",
            "booking_type":    b.booking_type.type_name,
            "start_date":      b.start_date.isoformat() if b.start_date else None,
            "end_date":        b.end_date.isoformat() if b.end_date else None,
            "number_of_people": b.number_of_people,
            "total_amount":    float(b.total_amount),
            "status":          b.status,
        })
    return result, 200


# ------------------------------------------------------------------ #
# OWNER → Approve / Reject booking
# ------------------------------------------------------------------ #
def update_booking_status_service(owner_id, booking_id, status):
    if status not in ["confirmed", "cancelled"]:
        return {"error": "Invalid status. Use 'confirmed' or 'cancelled'"}, 400

    try:
        uid = uuid.UUID(str(owner_id))
    except (ValueError, AttributeError):
        return {"error": "Invalid owner identity"}, 401

    booking = (
        Booking.query
        .join(Space, Booking.space_id == Space.space_id)
        .filter(Booking.booking_id == booking_id, Space.owner_id == uid)
        .first()
    )
    if not booking:
        return {"error": "Booking not found or you are not the owner"}, 404

    if booking.status != "pending":
        return {"error": "Only pending bookings can be updated"}, 400

    try:
        booking.status = status
        if status == "cancelled":
            booking.cancelled_at = datetime.utcnow()
        db.session.commit()
        return {
            "message": f"Booking {status} successfully",
            "booking_id": str(booking.booking_id),
            "status": booking.status,
        }, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Internal server error", "details": str(e)}, 500


# ------------------------------------------------------------------ #
# USER → Get all bookings (history)
# ------------------------------------------------------------------ #
def get_user_bookings_service(user_id):
    try:
        uid = uuid.UUID(str(user_id))
    except (ValueError, AttributeError):
        return {"bookings": []}, 200

    bookings = (
        Booking.query
        .filter_by(user_id=uid)
        .order_by(Booking.created_at.desc())
        .all()
    )
    result = []
    for b in bookings:
        result.append({
            "booking_id":      str(b.booking_id),
            "space_name":      b.space.space_name,
            "booking_type":    b.booking_type.type_name,
            "start_date":      b.start_date.isoformat() if b.start_date else None,
            "end_date":        b.end_date.isoformat() if b.end_date else None,
            "number_of_people": b.number_of_people,
            "total_amount":    float(b.total_amount),
            "status":          b.status,
        })
    return {"bookings": result}, 200


# ------------------------------------------------------------------ #
# USER → Cancel own booking
# ------------------------------------------------------------------ #
def cancel_booking_service(user_id, booking_id):
    try:
        uid = uuid.UUID(str(user_id))
    except (ValueError, AttributeError):
        return {"error": "Invalid user identity"}, 401

    booking = Booking.query.filter_by(
        booking_id=booking_id, user_id=uid
    ).first()
    if not booking:
        return {"error": "Booking not found"}, 404
    if booking.status not in ("pending", "confirmed"):
        return {"error": "Only pending or confirmed bookings can be cancelled"}, 400

    booking.status = "cancelled"
    booking.cancelled_at = datetime.utcnow()
    try:
        db.session.commit()
        return {
            "message": "Booking cancelled successfully",
            "booking_id": str(booking.booking_id),
            "status": booking.status,
        }, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Internal server error", "details": str(e)}, 500

from app.extensions import db
from app.models.bookings import Booking
from app.models.spaces import Space
from app.models.booking_types import BookingType
from app.models.space_pricing import SpacePricing
from datetime import datetime
from decimal import Decimal
import math
import uuid

#User create booking
def create_booking_service(user_id, data):
    try:
        #Required_fields
        required_fields =[
            "space_id",
            "booking_type_id",
            "start_date",
            "end_date",
            "number_of_people"
        ]

        for field in required_fields:
            if field not in data:
                return{"error":f"{field} is required"}, 400
        
        try:
            space_id = uuid.UUID(data["space_id"])
        except(ValueError):
            return{"error":"Invalid space_id format"}, 400
        
        booking_type_id = data["booking_type_id"]

        try:
            number_of_people = int(data["number_of_people"])
        except(ValueError, TypeError):
            return {"error":"number_of _people must be an integer"}, 400

        # Check Dates
        try:
            start_date = datetime.fromisoformat(data["start_date"])
            end_date = datetime.fromisoformat(data["end_date"])
        except ValueError:
            return{"error":"Invalid date format. use ISO format"}, 400
        
        if end_date<= start_date:
            return{"error":"end_date must be after start_date"}, 400
        
        # Check space exists & is ACTIVE
        space = Space.query.filter_by(space_id=space_id,approval_status="active").first()

        if not space:
            return {"error": "Space not available for booking"}, 404

        # Capacity check
        if number_of_people > space.max_capacity:
            return {"error": "Exceeds space capacity"}, 400

        # Check booking type
        booking_type = BookingType.query.get(booking_type_id)
        if not booking_type:
            return {"error": "Invalid booking type"}, 400

        # Check pricing exists for space
        pricing = SpacePricing.query.filter_by(
            space_id=space_id,
            price_type=booking_type.type_name.lower()
        ).first()

        if not pricing:
            return {
                "error": f"No pricing available for {booking_type.type_name}"
            }, 400

        # Prevent overlapping bookings
        overlapping = Booking.query.filter(
            Booking.space_id == space_id,
            Booking.status != "cancelled",
            Booking.start_date < end_date,
            Booking.end_date > start_date
        ).first()

        if overlapping:
            return {"error": "Space already booked for this time"}, 409

        # Calculate total amount
        duration_seconds = (end_date - start_date).total_seconds()
        price_per_unit = Decimal(str(pricing.price_amount))

        if booking_type.type_name == "hourly":
            duration_hours = math.ceil(duration_seconds/3600)
            total_amount = price_per_unit * Decimal(duration_hours)
        else:
            total_amount = price_per_unit

        # Create booking (PENDING – owner approval)
        booking = Booking(
            user_id=user_id,
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
            "booking_id": booking.booking_id,
            "status": booking.status,
            "total_amount": float(total_amount)
        }, 201

    except Exception as e:
        db.session.rollback()
        return {
            "error": "Internal server error",
            "details": str(e)
        }, 500
    
def get_owner_pending_bookings_service(owner_id):
    bookings = (
        Booking.query.join(Space, Booking.space_id == Space.space_id).filter(
            Space.owner_id == owner_id,
            Booking.status == "pending" 
        )
        .all()
    )

    result = []
    for booking in bookings:
        result.append({
            "booking_id": booking.booking_id,
            "space_id": booking.space_id,
            "user_id": booking.user_id,
            "start_date": booking.start_date,
            "end_date": booking.end_date,
            "total_amount": float(booking.total_amount),
            "status": booking.status
        })

    return result, 200 #OK
    
def update_booking_status_service(owner_id, booking_id, status):
    if status not in ["completed", "cancelled"]:
        return{
            "error":"Invalid status."
        }, 400
    
    booking = ( Booking.query.join(Space, Booking.space_id == Space.space_id)
               .filter(Booking.booking_id == booking_id, Space.owner_id == owner_id).first())
    if not booking:
        return{"error":"Booking not found or you are not the Owner"}, 404
    
    if booking.status != "pending":
        return{"error":"Only pending bookings can be updated"}, 400
    try:
        booking.status = status
        if status == "cancelled":
            booking.cancelled_at = datetime.utcnow()
        db.session.commit()

        return{
            "message":f"Booking{status} successfully",
            "booking_id": booking.booking_id,
            "status": booking.status
        }, 200
    except Exception as e:
        db.session.rollback()
        return{"message":"Internal Server error",
               "details": str(e)}, 500 
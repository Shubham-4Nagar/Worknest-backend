from app.extensions import db
from app.models.payments import Payment
from app.models.bookings import Booking
from app.services.notification_service import create_notification
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

ALLOWED_METHODS = ["UPI", "DEBITCARD", "CREDITCARD", "CASH"]

def create_payment_service(user_id, data):
    try:
        # Validate input
        required_fields = ["booking_id", "payment_method"]
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        booking_id = data["booking_id"]
        payment_method = data["payment_method"]

        # Validate payment method
        if payment_method not in ALLOWED_METHODS:
            return {
                "error": f"Invalid payment_method. Allowed: {ALLOWED_METHODS}"
            }, 400

        # Fetch booking
        booking = Booking.query.filter_by(
            booking_id=booking_id,
            user_id=user_id
        ).first()

        if not booking:
            return {"error": "Booking not found"}, 404

        # Payment only allowed for the pending bookings
        if booking.status != "pending":
            return {
                "error": "Payment allowed only for pending bookings"
            }, 400

        # Prevent duplicate payment
        if Payment.query.filter_by(booking_id=booking_id).first():
            return {"error": "Payment already done for this booking"}, 409

        # Amount validation
        amount = Decimal(str(booking.total_amount))
        if amount <= 0:
            return {"error": "Invalid payment amount"}, 400

        # Create payment
        payment = Payment(
            booking_id=booking_id,
            payment_method=payment_method,
            amount_paid=amount,
            payment_status="success"
        )

        #update the booking status
        booking.status = "completed"

        db.session.add(payment)
        db.session.commit() 

        # success notification 
        create_notification(
            user_id=booking.user_id,
            title="Payment Successful ",
            message=(
                f"Your payment of ₹{payment.amount_paid} "
                f"for booking #{booking.booking_id} was successful."
            )
        )

        return {
            "message": "Payment successful",
            "payment_id": payment.payment_id,
            "booking_id": booking_id,
            "amount_paid": str(payment.amount_paid),
            "status": payment.payment_status
        }, 201

    except IntegrityError:
        db.session.rollback()
        return {"error": "Duplicate payment"}, 409

    except Exception as e:
        db.session.rollback()
        return {
            "error": "Internal server error",
            "details": str(e)
        }, 500

import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint
from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    payment_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    booking_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("bookings.booking_id"),
        nullable=False,
        unique=True
    )

    payment_method = db.Column(
        db.Enum(
            "UPI",
            "DEBITCARD",
            "CREDITCARD",
            "CASH",
            name="payment_method_enum"
        ),
        nullable=False
    )

    currency = db.Column(
        db.String(10),
        server_default="INR",
        nullable=False
    )

    amount_paid = db.Column(
        db.Numeric(10, 2)
    )

    payment_status = db.Column(
        db.Enum(
            "success",
            "failed",
            "refunded",
            name="payment_status_enum"
        ),
        nullable=False,
        default="success"
    )

    payment_date = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "amount_paid > 0",
            name="payments_amount_paid_check"
        ),
    )

    # Relationship
    booking = db.relationship(
        "Booking",
        back_populates="payments")

import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint
from app.extensions import db



class Booking(db.Model):
    __tablename__ = "bookings"

    booking_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    space_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("spaces.space_id"),
        nullable=False
    )

    booking_type_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("booking_types.booking_type_id"),
        nullable=False
    )

    start_date = db.Column(
        db.DateTime,
        nullable=False
    )

    end_date = db.Column(
        db.DateTime,
        nullable=False
    )

    number_of_people = db.Column(
        db.Integer,
        default=1
    )

    total_amount = db.Column(
        db.Numeric(10, 2)
    )

    status = db.Column(
        db.Enum(
            "pending",
            "confirmed",
            "completed",
            "cancelled",
            name="booking_status_enum"
        ),
        nullable=False,
        default="pending"
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

    cancelled_at = db.Column(
        db.DateTime,
        nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "total_amount >= 0",
            name="bookings_total_amount_check"
        ),
    )

    # Relationships
    user = db.relationship(
        "User",
        back_populates="bookings"
    )

    space = db.relationship(
        "Space",
        back_populates="bookings"
    )

    booking_type = db.relationship(
        "BookingType",
        back_populates="bookings"
    )

    payments = db.relationship(
        "Payment",
        back_populates="booking",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="booking",
        cascade="all, delete-orphan"
    )

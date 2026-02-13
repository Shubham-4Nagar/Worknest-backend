import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.extensions import db


class BookingType(db.Model):
    __tablename__ = "booking_types"

    booking_type_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    type_name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
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

    # Relationship
    bookings = db.relationship(
        "Booking",
        back_populates="booking_type")
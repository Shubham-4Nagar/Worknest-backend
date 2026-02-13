import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint
from app.extensions import db


class Review(db.Model):
    __tablename__ = "review"

    review_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    booking_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("bookings.booking_id"),
        nullable=False
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

    rating = db.Column(
        db.Integer,
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
    __table_args__ = (
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="review_rating_check"
        ),
    )

    # Relationships
    booking = db.relationship(
        "Booking",
        back_populates="reviews"
    )

    user = db.relationship(
        "User",
        back_populates="reviews"
    )

    space = db.relationship(
        "Space",
        back_populates="reviews")

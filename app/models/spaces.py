import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,Text,Boolean,ForeignKey,Integer
from sqlalchemy.sql import func
from app.extensions import db


class Space(db.Model):
    __tablename__ = "spaces"

    space_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    owner_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    space_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(Text, nullable=True)

    max_capacity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=False
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

    # Relationships
    owner = db.relationship(
        "User",
        back_populates="spaces"
    )

    pricing = db.relationship(
        "SpacePricing",
        back_populates="space",
        cascade="all, delete-orphan"
    )
    bookings = db.relationship(
        "Booking",
        back_populates="space",
        cascade ="all, delete-orphan"
    )

    amenities = db.relationship(
        "SpaceAmenity",
        back_populates="space",
        cascade="all, delete-orphan"
    )
    
    reviews = db.relationship(
    "Review",
    back_populates="space",
    cascade="all, delete-orphan"
    )

    wishlist = db.relationship(
    "Wishlist",
    back_populates="space",
    cascade="all, delete-orphan"
    )



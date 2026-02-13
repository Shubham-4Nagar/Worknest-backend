import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.extensions import db


class Amenity(db.Model):
    __tablename__ = "amenities"

    amenity_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    amenity_name = db.Column(
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

    # Relationship (Many-to-Many via bridge)
    spaces = db.relationship(
        "SpaceAmenity",
        back_populates="amenity",
        cascade="all, delete-orphan"
    )

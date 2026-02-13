from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.extensions import db


class SpaceAmenity(db.Model):
    __tablename__ = "space_amenities"

    space_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("spaces.space_id"),
        primary_key=True
    )

    amenity_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("amenities.amenity_id"),
        primary_key=True
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
    space = db.relationship(
        "Space",
        back_populates="amenities"
    )

    amenity = db.relationship(
        "Amenity",
        back_populates="spaces"
    )
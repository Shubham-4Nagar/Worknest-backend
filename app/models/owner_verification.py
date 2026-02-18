import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.extensions import db


class OwnerVerification(db.Model):
    __tablename__ = "owner_verification"

    verification_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    owner_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    id_proof = db.Column(
        db.String(255),
        nullable=False
    )

    status = db.Column(
        db.Enum(
            "pending",
            "approved",
            "rejected",
            name="owner_status_enum"  
        ),
        nullable=False,
        default="pending"
    )

    verified_by = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.user_id"),
        nullable=True
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
        foreign_keys=[owner_id],
        back_populates="owner_verification"
    )

    verifier = db.relationship(
        "User",
        foreign_keys=[verified_by]
    )
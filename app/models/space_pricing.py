import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint
from app.extensions import db


class SpacePricing(db.Model):
    __tablename__ = "spaces_pricing"

    pricing_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    space_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("spaces.space_id"),
        nullable=False
    )

    price_type = db.Column(
        db.Enum(
            "hourly",
            "daily",
            "weekly",
            "monthly",
            name="pricing_type_enum"
        ),
        nullable=False
    )

    price_amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    # Relationships
    space = db.relationship(
        "Space",
        back_populates="pricing"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "space_id",
            "price_type",
            name="unique_space_price_types"
        ),
        CheckConstraint(
            "price_amount > 0",
            name="check_price_amount_positive"
        ),
    )
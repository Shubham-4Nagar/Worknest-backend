import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.extensions import db


class Wishlist(db.Model):
    __tablename__ = "wishlist"

    wishlist_id = db.Column(
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
    db.UniqueConstraint("user_id", "space_id", name="unique_user_space_wishlist"),
)


    # Relationships
    user = db.relationship(
        "User",
        back_populates="wishlist"
    )
    space = db.relationship(
        "Space",
        back_populates="wishlist")

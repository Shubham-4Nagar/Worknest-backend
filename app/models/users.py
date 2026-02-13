import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    role_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("roles.role_id"),
        nullable=False
    )

    phone_number = db.Column(db.String(20))
    profile_image = db.Column(db.String(100))

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
    role = db.relationship("Role", back_populates="users")
    bookings = db.relationship("Booking", back_populates="user")
    spaces = db.relationship("Space", back_populates="owner", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="user")
    wishlist = db.relationship("Wishlist", back_populates="user")
    notifications = db.relationship("Notification", back_populates="user")
    owner_verification = db.relationship(
        "OwnerVerification",
        back_populates="owner",
        uselist=False
    )

    # Password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
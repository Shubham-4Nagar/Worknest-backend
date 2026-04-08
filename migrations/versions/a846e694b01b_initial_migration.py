"""initial migration

Revision ID: a846e694b01b
Revises:
Create Date: 2026-02-17 15:48:19.823749

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "a846e694b01b"
down_revision = None
branch_labels = None
depends_on = None


booking_status_enum = postgresql.ENUM(
    "pending",
    "confirmed",
    "completed",
    "cancelled",
    name="booking_status_enum",
    create_type=False,
)
owner_status_enum = postgresql.ENUM(
    "pending",
    "approved",
    "rejected",
    name="owner_status_enum",
    create_type=False,
)
payment_method_enum = postgresql.ENUM(
    "UPI",
    "DEBITCARD",
    "CREDITCARD",
    "CASH",
    name="payment_method_enum",
    create_type=False,
)
payment_status_enum = postgresql.ENUM(
    "success",
    "failed",
    "refunded",
    name="payment_status_enum",
    create_type=False,
)
pricing_type_enum = postgresql.ENUM(
    "hourly",
    "daily",
    "weekly",
    "monthly",
    name="pricing_type_enum",
    create_type=False,
)
space_type_enum = postgresql.ENUM(
    "private_cabin",
    "hot_desk",
    "meeting_room",
    "event_space",
    name="space_type_enum",
    create_type=False,
)


def upgrade():
    bind = op.get_bind()
    booking_status_enum.create(bind, checkfirst=True)
    owner_status_enum.create(bind, checkfirst=True)
    payment_method_enum.create(bind, checkfirst=True)
    payment_status_enum.create(bind, checkfirst=True)
    pricing_type_enum.create(bind, checkfirst=True)
    space_type_enum.create(bind, checkfirst=True)

    op.create_table(
        "roles",
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_name", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("role_id"),
        sa.UniqueConstraint("role_name"),
    )

    op.create_table(
        "booking_types",
        sa.Column("booking_type_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("type_name", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("booking_type_id"),
        sa.UniqueConstraint("type_name"),
    )

    op.create_table(
        "amenities",
        sa.Column("amenity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amenity_name", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("amenity_id"),
        sa.UniqueConstraint("amenity_name"),
    )

    op.create_table(
        "users",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reset_token", sa.String(length=255), nullable=True),
        sa.Column("reset_token_expiry", sa.DateTime(), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.Column("profile_image", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["roles.role_id"]),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "spaces",
        sa.Column("space_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("space_name", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("max_capacity", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("space_type", space_type_enum, nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("space_id"),
    )

    op.create_table(
        "owner_verification",
        sa.Column("verification_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_proof", sa.String(length=255), nullable=False),
        sa.Column("status", owner_status_enum, server_default=sa.text("'pending'"), nullable=False),
        sa.Column("verified_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["verified_by"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("verification_id"),
    )

    op.create_table(
        "notifications",
        sa.Column("notification_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("message", sa.String(length=255), nullable=False),
        sa.Column("is_read", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("notification_id"),
    )

    op.create_table(
        "bookings",
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("space_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("booking_type_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=False),
        sa.Column("number_of_people", sa.Integer(), nullable=True),
        sa.Column("total_amount", sa.Numeric(10, 2), nullable=True),
        sa.Column("status", booking_status_enum, server_default=sa.text("'pending'"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("total_amount >= 0", name="bookings_total_amount_check"),
        sa.ForeignKeyConstraint(["booking_type_id"], ["booking_types.booking_type_id"]),
        sa.ForeignKeyConstraint(["space_id"], ["spaces.space_id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("booking_id"),
    )

    op.create_table(
        "payments",
        sa.Column("payment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("payment_method", payment_method_enum, nullable=False),
        sa.Column("currency", sa.String(length=10), server_default=sa.text("'INR'"), nullable=False),
        sa.Column("amount_paid", sa.Numeric(10, 2), nullable=True),
        sa.Column("payment_status", payment_status_enum, server_default=sa.text("'success'"), nullable=False),
        sa.Column("payment_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.CheckConstraint("amount_paid > 0", name="payments_amount_paid_check"),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.booking_id"]),
        sa.PrimaryKeyConstraint("payment_id"),
        sa.UniqueConstraint("booking_id"),
    )

    op.create_table(
        "review",
        sa.Column("review_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("space_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.CheckConstraint("rating >= 1 AND rating <= 5", name="review_rating_check"),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.booking_id"]),
        sa.ForeignKeyConstraint(["space_id"], ["spaces.space_id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("review_id"),
    )

    op.create_table(
        "space_amenities",
        sa.Column("space_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amenity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["amenity_id"], ["amenities.amenity_id"]),
        sa.ForeignKeyConstraint(["space_id"], ["spaces.space_id"]),
        sa.PrimaryKeyConstraint("space_id", "amenity_id"),
    )

    op.create_table(
        "spaces_pricing",
        sa.Column("pricing_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("space_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("price_type", pricing_type_enum, nullable=False),
        sa.Column("price_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.CheckConstraint("price_amount > 0", name="check_price_amount_positive"),
        sa.ForeignKeyConstraint(["space_id"], ["spaces.space_id"]),
        sa.PrimaryKeyConstraint("pricing_id"),
        sa.UniqueConstraint("space_id", "price_type", name="unique_space_price_types"),
    )

    op.create_table(
        "wishlist",
        sa.Column("wishlist_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("space_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["space_id"], ["spaces.space_id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("wishlist_id"),
        sa.UniqueConstraint("user_id", "space_id", name="unique_user_space_wishlist"),
    )


def downgrade():
    op.drop_table("wishlist")
    op.drop_table("spaces_pricing")
    op.drop_table("space_amenities")
    op.drop_table("review")
    op.drop_table("payments")
    op.drop_table("bookings")
    op.drop_table("notifications")
    op.drop_table("owner_verification")
    op.drop_table("spaces")
    op.drop_table("users")
    op.drop_table("amenities")
    op.drop_table("booking_types")
    op.drop_table("roles")

    bind = op.get_bind()
    space_type_enum.drop(bind, checkfirst=True)
    pricing_type_enum.drop(bind, checkfirst=True)
    payment_status_enum.drop(bind, checkfirst=True)
    payment_method_enum.drop(bind, checkfirst=True)
    owner_status_enum.drop(bind, checkfirst=True)
    booking_status_enum.drop(bind, checkfirst=True)

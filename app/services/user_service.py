from app.extensions import db
from app.models.users import User
from app.models.roles import Role
from app.models.owner_verification import OwnerVerification
from sqlalchemy.exc import IntegrityError


def register_user(data):

    # 1. Required fields validation
    required_fields = ["first_name", "last_name", "email", "password"]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    # 2. Check if user already exists
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        raise ValueError("Email already registered")

    # 3. Get default role
    user_role = Role.query.filter_by(role_name="User").first()
    if not user_role:
        raise RuntimeError("User role not configured")

    # 4. Create user
    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        role_id=user_role.role_id
    )

    new_user.set_password(data["password"])

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user

    except IntegrityError:
        db.session.rollback()
        raise ValueError("Database integrity error")

    except Exception:
        db.session.rollback()
        raise RuntimeError("Internal server error")


# Owner verification
def request_owner_service(user_id, data):

    if "id_proof" not in data:
        raise ValueError("ID proof required")

    existing = OwnerVerification.query.filter_by(owner_id=user_id).first()
    if existing:
        raise ValueError("Request already exists")

    owner_request = OwnerVerification(
        owner_id=user_id,
        id_proof=data["id_proof"],
        status="pending"
    )

    try:
        db.session.add(owner_request)
        db.session.commit()
        return owner_request

    except Exception:
        db.session.rollback()
        raise RuntimeError("Internal server error")
    
# Update user profile
def update_user_profile_service(user_id, data):
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    if "first_name" in data:
        first_name = data["first_name"].strip()
        if not first_name:
            raise ValueError("first_name cannot be empty")
        user.first_name = first_name

    if "last_name" in data:
        last_name = data["last_name"].strip()
        if not last_name:
            raise ValueError("last_name cannot be empty")
        user.last_name = last_name

    if "phone_number" in data:
        user.phone_number = data["phone_number"].strip()

    if "profile_image" in data:
        user.profile_image = data["profile_image"].strip()

    try:
        db.session.commit()
        return {
            "message": "Profile updated successfully",
            "user_id": str(user.user_id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "profile_image": user.profile_image
        }
    except Exception:
        db.session.rollback()
        raise RuntimeError("Internal server error")
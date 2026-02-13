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
def request_owner(user_id, data):

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

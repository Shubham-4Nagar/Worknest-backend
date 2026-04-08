import secrets
from datetime import datetime, timedelta
from flask import current_app
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.users import User


#Login process
def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"error": "Invalid email or password"}, 401

    token = create_access_token(identity=str(user.user_id))

    return{
        "user_id": str(user.user_id),
        "role":user.role.role_name,
        "access_token": token
    }, 200

def get_current_user(user_id):
    
    user = User.query.get(user_id)

    if not user:
        raise ValueError("User not found")
    
    return user

def forgot_password(email):
    user =User.query.filter_by(email=email).first()

    response = {
        "message": "If the email is registered, a password reset link has been generated"
    }

    if not user:
        return response, 200
    
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow()+ timedelta(minutes=30)

    try:
        user.reset_token = token
        user.reset_token_expiry = expiry
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "Unable to process password reset request"}, 500

    if current_app.config.get("PASSWORD_RESET_TOKEN_EXPOSE"):
        response["reset_token"] = token

    return response, 200

def reset_password(token, new_password):
    user = User.query.filter_by(reset_token=token).first()

    if not user:
        return {"error": "Invalid token"}, 400

    if not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        return {"error": "Token expired"}, 400

    try:
        user.set_password(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "Unable to reset password"}, 500

    return {"message": "Password reset successful"}, 200

#logout
def logout_user():
    return True

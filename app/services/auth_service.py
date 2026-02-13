from flask_jwt_extended import create_access_token
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
        "token": token
    }

def get_current_user(user_id):
    
    user = User.query.get(user_id)

    if not user:
        raise ValueError("User not found")
    
    return user

def logout_user():
    return True

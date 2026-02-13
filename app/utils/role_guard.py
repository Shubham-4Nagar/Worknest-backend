from functools import wraps
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask import jsonify
from app.models.users import User

@jwt_required()
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role.role_name != "Admin":
            return jsonify({"error":"Admin access required"}), 403
        
        return fn(*args, **kwargs)
    return wrapper

@jwt_required()
def owner_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role.role_name != "Owner":
            return jsonify({"error":"Owner access required"}), 403 #Forbidden
        return fn(*args, **kwargs)
    return wrapper
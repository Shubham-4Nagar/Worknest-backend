from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import login_user, get_current_user


def login():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    try:
        result = login_user(email, password)

        return jsonify({
            "message": "Login successful",
            **result
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@jwt_required()
def me():

    user_id = get_jwt_identity()

    try:
        user = get_current_user(user_id)

        return jsonify({
            "user_id": str(user.user_id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role.role_name
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception:
        return jsonify({"error": "Internal server error"}), 500
    
from flask_jwt_extended import jwt_required


@jwt_required()
def logout():
    return jsonify({
        "message": "Logged out successfully"
    }), 200


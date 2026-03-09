from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import (
    register_user,
    request_owner_service,
    update_user_profile_service
)


def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        user = register_user(data)

        return jsonify({
            "message": "User registered successfully",
            "user_id": str(user.user_id)
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        print("REGISTER ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


@jwt_required()
def request_owner_controller():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        request_owner_service(user_id, data)

        return jsonify({
            "message": "Owner request submitted successfully"
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@jwt_required()
def update_my_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        result = update_user_profile_service(user_id, data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
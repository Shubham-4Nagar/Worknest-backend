from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import register_user, request_owner


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

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@jwt_required()
def request_owner():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        request_owner(user_id, data)

        return jsonify({
            "message": "Owner request submitted successfully"
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    except Exception:
        return jsonify({"error": "Internal server error"}), 500

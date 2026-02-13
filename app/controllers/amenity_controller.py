from flask import request, jsonify
from app.services.amenity_service import(
    create_amenity_service,
    list_amenities_service # these are the classes we made
)

def create_amenity():
    data = request.get_json()

    if not data:
        return jsonify({"error":"Invalid JSON body"}), 400
    
    result, status = create_amenity_service(data)
    return jsonify(result), status

def list_amenities():
    result, status = list_amenities_service()
    return jsonify(result), status
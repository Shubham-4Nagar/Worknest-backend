from app.extensions import db
from app.models.amenities import Amenity
from sqlalchemy.exc import IntegrityError

def create_amenity_service(data):
    try:
        if not data or "amenity_name" not in data:
            return{"error":"amenity_name is required"}, 400 # Bad request
        
        amenity_name = data["amenity_name"].strip().title()

        if not amenity_name:
            return{"error":"amenity_name cannot be empty"}, 400
        
        existing = Amenity.query.filter_by(amenity_name=amenity_name).first()
        if existing:
            return{"error":"Amenity already exists"}, 409
        
        #Create amenity
        amenity = Amenity(
            amenity_name = amenity_name
        )

        db.session.add(amenity)
        db.session.commit()

        return{
            "message":"Amenity_created_successfully",
            "amenity_id": amenity.amenity_id,
            "amenity_name": amenity.amenity_name
        }, 201 # created
    
    except IntegrityError:
        db.session.rollback()
        return{"error":"Amenity already exits"
               }, 409 # Conflict
    
    except Exception as e:
        db.session.rollback()
        return{
            "error": "Internal server error",
            "details": str(e)
        }, 500 # Server error
    
def list_amenities_service():
    amenities = Amenity.query.order_by(Amenity.amenity_name.asc()).all()

    result = []
    for amenity in amenities:
        result.append({
            "amenity_id": amenity.amenity_id,
            "amenity_name":amenity.amenity_name
        })

    return result, 200 #OK
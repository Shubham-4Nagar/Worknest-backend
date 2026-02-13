from app.extensions import db
from app.models.reviews import Review
from app.models.bookings import Booking
from sqlalchemy.exc import IntegrityError

def create_review_service(user_id, data):
    try:
        required = ["booking_id", "space_id", "rating"]
        for field in required:
            if field not in data:
                return {"error": f"{field} is required"}, 400
        
        booking_id = data["booking_id"]
        space_id = data["space_id"]
    
        try:
            rating = int(data["rating"])
        except (ValueError, TypeError):
            return{
                "error":"rating must be Integer"
                }, 400
        if rating < 1 or rating > 5:
            return{"error":"RAting must be between 1 and 5"}, 400

        booking = Booking.query.filter_by(
            booking_id=booking_id,
            user_id=user_id,
            space_id=space_id,
            status="completed"
        ).first()

        if not booking:
            return {"error": "Completed booking not found"}, 404
    
        #Preventing duplicate review for one space from one user
        existing = Review.query.filter_by(booking_id=booking_id).first()
        if existing:
            return {"error": "Review already submitted"}, 409
 
        review = Review(
            booking_id=booking_id,
            user_id=user_id,
            space_id=space_id,
            rating=rating
        )

        db.session.add(review)
        db.session.commit()

        return {
            "message": "Review submitted successfully",
            "rating": rating
        }, 201
    except IntegrityError:
        db.session.rollback()
        return{"error":"Duplicate error"}, 409
    except Exception as e:
        db.session.rollback()
        return{
            "message":"Internal Server Error",
            "details": str(e)
        }


def get_space_reviews_service(space_id):
    reviews = Review.query.filter_by(space_id=space_id).all()

    result = []
    for r in reviews:
        result.append({
            "review_id": r.review_id,
            "user_id": r.user_id,
            "rating": r.rating,
            "created_at": r.created_at.isoformat()
        })

    return result, 200

def get_user_reviews_service(user_id):
    reviews = Review.query.filter_by(user_id=user_id).all()

    result = []
    for r in reviews:
        result.append({
            "review_id": r.review_id,
            "space_id": r.space_id,
            "rating": r.rating,
            "created_at": r.created_at.isoformat()
        })

    return result, 200

from app.extensions import db
from app.models.wishlist import Wishlist
from app.models.spaces import Space
from sqlalchemy.exc import IntegrityError

def add_to_wishlist_service(user_id, space_id):
    try:
        space = Space.query.filter_by(
            space_id=space_id,
            approval_status = "active"
        ).first()

        if not space:
            return{"error":"Space not available"}, 404
        
        wishlist = Wishlist(
            user_id=user_id,
            space_id =space_id
        )

        db.session.add(wishlist)
        db.session.commit()

        return{
            "message":"Space added to wishlist",
            "space_id": space_id
        }, 201
    
    except IntegrityError:
        db.session.rollback()
        return{"error":"Space already in wishlist"}, 409
    except Exception as e:
        db.session.rollback()
        return{
            "message":"Internal Server error",
            "details": str(e)
        }

def get_user_wishlist_service(user_id):
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()

    result = []

    for item in wishlist_items:
        result.append({
            "wishlist_id": item.wishlist_id,
            "space_id": item.space_id,
            "created_at": item.created_at.isoformat()
        })

        return result, 200
    
def remove_from_wishlist_service(user_id, space_id):
    wishlist = Wishlist.query.filter_by(
        user_id=user_id,
        space_id=space_id
    ).first()

    if not wishlist:
        return {"error":"Space not found in wishlist"}, 404
    
    db.session.delete(wishlist)
    db.session.commit()

    return{
        "message":"Removed from Wishlist",
        "space_id": space_id
    }, 200 # ok
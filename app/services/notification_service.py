from app.extensions import db
from app.models.notifications import Notification


#Creating notification for the user
def create_notification(user_id, title, message):
    try:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message
        )

        db.session.add(notification)
        db.session.commit()
        
        return notification

    except Exception as e:
        db.session.rollback()
        return {
            "message":"Internal server error",
            "details": str(e)
        }


#Fetch all the notification for the user order by lastest one first
def get_user_notifications_service(user_id):
    notification = (
        Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    )

    result = []
    for n in notification:
        result.append({
            "notification_id": n.notification_id,
            "title": n.title,
            "message": n.message,
            "created_at": n.created_at.isoformat()
        })

    return result, 200 #OK
        

    
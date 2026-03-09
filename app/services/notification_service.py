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

#Mark a single notification as read
def mark_notification_read_service(user_id, notification_id):
    notification = Notification.query.filter_by(
        notification_id=notification_id,
        user_id=user_id
    ).first()

    if not notification:
        return {"error": "Notification not found"}, 404

    notification.is_read = True
    db.session.commit()

    return {"message": "Notification marked as read"}, 200


# Mark ALL notifications as read for a user
def mark_all_notifications_read_service(user_id):
    Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).update({"is_read": True})

    db.session.commit()

    return {"message": "All notifications marked as read"}, 200
        

    
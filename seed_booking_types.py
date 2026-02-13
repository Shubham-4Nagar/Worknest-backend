from app import create_app
from app.extensions import db
from app.models.booking_types import BookingType

app = create_app()

with app.app_context():
    try:
        types = ["hourly","daily","weekly","monthly"]

        for type_name in types:
            existing = BookingType.query.filter_by(type_name=type_name).first()

            if not existing:
                db.session.add(BookingType(type_name=type_name))
                print(f"Added booking types: {type_name}")
            else:
                print(f"Already exists: {type_name}")

        db.session.commit()
        print("\n Booking types seeded successfully")

    except Exception as e:
        db.session.rollback()
        print("\n Error seeding booking types:", e)
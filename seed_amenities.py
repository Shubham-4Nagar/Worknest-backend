from app import create_app
from app.extensions import db
from app.models.amenities import Amenity

app = create_app()

with app.app_context():
    try:
        amenities = [
            "WiFi",
            "Parking",
            "Air Conditioning",
            "Meeting Room",
            "Cafeteria",
            "Power Backup"
        ]

        for name in amenities:
            existing = Amenity.query.filter_by(amenity_name=name).first()

            if not existing:
                db.session.add(Amenity(amenity_name=name))
                print(f"Added amenity: {name}")
            else:
                print(f"Already exists: {name}")

        db.session.commit()
        print("\n✅ Amenities seeded successfully")

    except Exception as e:
        db.session.rollback()
        print("\n❌ Error seeding amenities:", e)

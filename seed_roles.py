from app import create_app
from app.extensions import db
from app.models.roles import Role

# Create app
app = create_app()

with app.app_context():
    try:
        roles = ["Admin","Owner","User"]

        for role_name in roles:
            existing_role = Role.query.filter_by(role_name=role_name).first()

            if not existing_role:
                db.session.add(Role(role_name=role_name))
                print(f"Added role: {role_name}")
            else:
                print(f"Role already exists: {role_name}")
        db.session.commit()
        print("\n Roles seeded successfully")

    except Exception as e:
        db.session.rollback()
        print("\n Error seeding roles:", e)
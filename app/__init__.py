from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.config import Config
from app.extensions import db, bcrypt, jwt

from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.admin_routes import admin_bp
from app.routes.space_routes import space_bp
from app.routes.space_pricing_routes import space_pricing_bp
from app.routes.admin_space_routes import admin_space_bp
from app.routes.booking_routes import booking_bp
from app.routes.amenity_routes import amenity_bp
from app.routes.space_amenity_routes import space_amenity_bp
from app.routes.payment_routes import payment_bp
from app.routes.notification_routes import notification_bp
from app.routes.wishlist_routes import wishlist_bp
from app.routes.review_routes import review_bp
from app.routes.owner_routes import owner_bp


migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    migrate.init_app(app, db)
   #REGISTER BLUEPRINTS
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(space_bp)
    app.register_blueprint(space_pricing_bp)
    app.register_blueprint(admin_space_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(amenity_bp)
    app.register_blueprint(space_amenity_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(owner_bp)

    @app.route("/health")
    def health():
        return{"status":"OK"}, 200
    
    @app.errorhandler(404)
    def not_found(e):
        return {"error":"Route not found"}, 404

    return app


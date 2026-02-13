from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Database ORM
db = SQLAlchemy()

#PASSWORD HASHING
bcrypt = Bcrypt()

#JWT authentication manager
jwt = JWTManager()

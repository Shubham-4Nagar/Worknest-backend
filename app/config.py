import os
from dotenv import load_dotenv

load_dotenv()#load variables from .env file

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    #JWT secret_key used for login & protected routes
    PASSWORD_RESET_TOKEN_EXPOSE = (
        os.getenv("PASSWORD_RESET_TOKEN_EXPOSE", "false").lower() == "true"
    )

    _database_url = os.getenv("DATABASE_URL")
    _db_parts = [
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("DB_NAME"),
    ]

    SQLALCHEMY_DATABASE_URI = _database_url or (
        f"postgresql://{_db_parts[0]}:"
        f"{_db_parts[1]}@"
        f"{_db_parts[2]}:"
        f"{_db_parts[3]}/"
        f"{_db_parts[4]}"
        if all(_db_parts) else None
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def validate(cls):
        missing = []

        if not cls.SECRET_KEY:
            missing.append("SECRET_KEY")
        if not cls.JWT_SECRET_KEY:
            missing.append("JWT_SECRET_KEY")
        if not cls.SQLALCHEMY_DATABASE_URI:
            missing.append("DATABASE_URL or DB_USER/DB_PASSWORD/DB_HOST/DB_PORT/DB_NAME")

        if missing:
            raise RuntimeError(
                "Missing required configuration: " + ", ".join(missing)
            )

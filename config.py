import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_APP = os.getenv("FLASK_APP")
    FLASK_ENV = os.getenv("FLASK_ENV")
    DEBUG = FLASK_ENV == "development"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

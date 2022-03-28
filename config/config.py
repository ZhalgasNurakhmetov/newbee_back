from pydantic import BaseSettings
import os


class DevelopmentConfig(BaseSettings):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY: str = os.getenv('START_UP_KEY')
    ALGORITHM: str = "HS256"
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URI_COM')
    ACCESS_TOKEN_EXPIRE_WEEKS: int = 1


config = DevelopmentConfig()

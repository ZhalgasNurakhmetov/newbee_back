from pydantic import BaseSettings
import os


class DevelopmentConfig(BaseSettings):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY: str = os.getenv('START_UP_KEY')
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URI_COM')


config = DevelopmentConfig()

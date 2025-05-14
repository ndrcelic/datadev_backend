import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    print(SQLALCHEMY_DATABASE_URI)


class DockerConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:nikola@db:5432/dd_database"
    UPLOAD_FOLDER = '/uploads'

config_by_name = {
    'development': DevelopmentConfig,
    'docker': DockerConfig,
}
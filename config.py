import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DockerConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:nikola@db:5432/dd_database"
    UPLOAD_FOLDER = '/app/uploads'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config_by_name = {
    'development': DevelopmentConfig,
    'docker': DockerConfig,
    'testing': TestConfig,
}
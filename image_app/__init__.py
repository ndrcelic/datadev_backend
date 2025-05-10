from flask import Flask
from image_app.resources import register_routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from .models import db
from .schemas import ms

#api = Api()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nikola@localhost:5432/datadev_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploads")

    db.init_app(app)
    ms.init_app(app)

    with app.app_context():
        Migrate(app, db)

    register_routes(app)
    return app
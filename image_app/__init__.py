from flask import Flask
from image_app.resources import register_routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from .models import db
from .schemas import ms
from flask_cors import CORS
from config import config_by_name

#api = Api()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    #CORS(app, resources={r"/images*": {"origins": "http://localhost:3000/images"}})

    app.config.from_object(config_by_name[config_name])

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nikola@localhost:5432/datadev_db'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploads")
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    ms.init_app(app)

    with app.app_context():
        Migrate(app, db)

    register_routes(app)
    return app
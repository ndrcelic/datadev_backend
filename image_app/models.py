from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(10), nullable=True)

    boxes = db.relationship('Box', backref='image', lazy=True)
    polygons = db.relationship('Polygon', backref='image', lazy=True)


class Box(db.Model):
    __tablename__ = 'boxes'
    id = db.Column(db.Integer, primary_key=True)
    x_point = db.Column(db.Float, nullable=False)
    y_point = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)

    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)


class Polygon(db.Model):
    __tablename__ = 'polygons'
    id = db.Column(db.Integer, primary_key=True)

    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)

    points = db.relationship('Point', backref='polygon', lazy=True)


class Point(db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True)
    x_point = db.Column(db.Float, nullable=False)
    y_point = db.Column(db.Float, nullable=False)
    ordinal = db.Column(db.Integer, nullable=False)

    polygon_id = db.Column(db.Integer, db.ForeignKey('polygons.id'), nullable=False)
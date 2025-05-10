from flask_marshmallow import Marshmallow
from .models import Image, Box, Polygon, Point
from marshmallow import fields, validate

ms = Marshmallow()


class BoxSchema(ms.SQLAlchemyAutoSchema):
    class Meta:
        model = Box
        load_instance = True
        include_fk = True

box_schema = BoxSchema()
boxes_schema = BoxSchema(many=True)


class PointSchema(ms.SQLAlchemyAutoSchema):
    class Meta:
        model = Point
        load_instance = True
        include_fk = True

point_schema = PointSchema()
points_schema = PointSchema(many=True)


class PolygonSchema(ms.SQLAlchemyAutoSchema):
    points = fields.Nested('PointSchema', many=True)

    class Meta:
        model = Polygon
        load_instance = True
        include_fk = True
        include_relationship = True

polygon_schema = PolygonSchema()
polygons_schema = PolygonSchema(many=True)


class ImageSchema(ms.SQLAlchemyAutoSchema):
    boxes = fields.Nested('BoxSchema', many=True)
    polygons = fields.Nested('PolygonSchema', many=True)

    class Meta:
        model = Image
        load_instance = True
        include_fk = True
        include_relationship = True

image_schema = ImageSchema()
images_schema = ImageSchema(many=True)
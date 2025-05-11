from flask_marshmallow import Marshmallow
from .models import Image, Box, Polygon, Point
from marshmallow import fields, validate
import os
import base64

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


class ImageAnnotationsSchema(ms.SQLAlchemyAutoSchema):
    boxes = fields.Nested('BoxSchema', many=True)
    polygons = fields.Nested('PolygonSchema', many=True)

    class Meta:
        model = Image
        load_instance = True
        include_fk = True
        include_relationship = True

image_annotations_schema = ImageAnnotationsSchema()
images_annotations_schema = ImageAnnotationsSchema(many=True)


class ImageSchema(ms.SQLAlchemyAutoSchema):
    row_image = fields.Method("get_row_image")

    class Meta:
        model = Image
        load_instance = True
        include_fk = True

    def get_row_image(self, obj):
        image_path = os.path.join('uploads', obj.url)
        if os.path.isfile(image_path):
            with open(image_path, 'rb') as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                mime = "image/jpeg" if image_path.endswith('.jpg') else "image/png"
                return f"data:{mime};base64,{encoded}"
        return None

image_schema = ImageSchema()
images_schema = ImageSchema(many=True)
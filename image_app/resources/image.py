from flask_restful import Resource, reqparse
from image_app.models import Image, Box, Polygon, Point, db
from image_app.schemas import images_schema,image_annotations_schema, ms
from flask import request, current_app, abort, Response
from werkzeug.utils import secure_filename
import os, json

class ImageResource(Resource):
    def post(self):
        if "file" not in request.files:
            return {"error" : "File is missing"}, 400

        file = request.files["file"]
        if file.filename == "":
            return {"error" : "File name is missing"}, 400

        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        extension = os.path.splitext(filename)[1]

        new_image = Image(url=upload_path, extension=extension)
        db.session.add(new_image)
        db.session.commit()

        print(new_image.id)
        return new_image.id, 201

    def get(self):
        images = Image.query.all()
        return images_schema.dump(images), 200


class ImageAnnotationResource(Resource):
    # proveriti sa verzijom ispod
    def post(self, image_id):
        data = request.get_json()

        shape_type = data.get('type')
        if not type:
            abort(400, description="Type is required")

        if shape_type == 'box':
            x_point = data.get('x')
            y_point = data.get('y')
            width = data.get('w')
            height = data.get('h')

            if x_point is None or y_point is None or width is None or height is None:
                abort(400, description="Some of values is/are missing'")


            if x_point < 0 or y_point < 0 or width < 0:
                abort(400, description="Some of values is/are more then 0.")

            box = Box.query.filter(Box.image_id==image_id, Box.x_point==x_point, Box.y_point==y_point, Box.width==width, Box.height==height).first()
            if box is not None:
                return {"error": "Box with that dimensions and points already exists!"}, 404

            box = Box(x_point=x_point, y_point=y_point, width=width, height=height, image_id=image_id)
            db.session.add(box)
            db.session.commit()

            return {"message": "Box", "x": x_point, "y": y_point, "width": width, "height": height}, 200
        elif shape_type == 'polygon':
            points = data.get('points')
            if points is None or len(points) == 0:
                abort(400, description="Points is missing")

            existence_list = []
            for i, point in enumerate(points):
                polygon = Polygon.query.filter(Polygon.image_id==image_id,
                                               Point.x_point==point[0],
                                               Point.y_point==point[1],
                                               ).join(Image).join(Point).first()

                if polygon is None:
                    existence_list.append(False)
                    break
                else:
                    existence_list.append(True)


            if len(existence_list) == len(points) and False not in existence_list:
                return {"error": "Polygon with that dimensions and points already exists!"}, 404

            polygon = Polygon(image_id=image_id)
            db.session.add(polygon)
            db.session.commit()

            new_points = []

            for i, point in enumerate(points):
                new_point = Point(
                    x_point=point[0],
                    y_point=point[1],
                    ordinal=i,
                    polygon_id=polygon.id
                )
                new_points.append(new_point)

            db.session.add_all(new_points)
            db.session.commit()

            return {"message" : "Image annotation created"}, 200
        else:
            abort(400, description=f"Type '{shape_type}' is not supported.")

    def get(self, image_id):
        image = Image.query.get(image_id)
        if image is None:
            return {"error" : "Image not found"}, 404
        return image_annotations_schema.dump(image), 200


class DownloadAnnotationsResource(Resource):
    def get(self, image_id):
        annotations = Image.query.get(image_id)
        if annotations is None:
            return {"error" : "Image not found"}, 404

        serialized_data = image_annotations_schema.dump(annotations)
        json_data = json.dumps(serialized_data, indent=4)

        response = Response(json_data, mimetype='application/json')
        response.headers['Content-Disposition'] = f'attachment; filename="image_{image_id}_annotations.json"'

        return response

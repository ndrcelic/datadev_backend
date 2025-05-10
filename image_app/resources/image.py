from flask_restful import Resource, reqparse
from image_app.models import Image, db
from image_app.schemas import images_schema, ms
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

class ImageResource(Resource):
    def post(self):
        print(request.files)
        if "file" not in request.files:
            return {"error" : "File is missing"}, 400

        file = request.files["file"]
        if file.filename == "":
            return {"error" : "File name is missing"}, 400

        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        #parser = reqparse.RequestParser()
        #parser.add_argument("url", type=str, required=True, help="URL is required")
        #parser.add_argument("annotation", type=str, required=False)

        #data = parser.parse_args()

        new_image = Image(url=upload_path, annotation="annotation")
        db.session.add(new_image)
        db.session.commit()

        return new_image.id, 201

    def get(self):
        images = Image.query.all()
        return images_schema.dump(images), 200
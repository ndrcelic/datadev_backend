import unittest
import json
from image_app import create_app
from image_app.models import db, Image, Box, Polygon, Point
from io import BytesIO
import os
from flask import current_app
from werkzeug.utils import secure_filename


class ImageAnnotationsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_post_new_image_success(self):
        payload = {
            'file': (BytesIO(b'test'), 'test_image.jpg'),
        }
        response = self.client.post('/images', data=payload, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 201)

        filename = secure_filename("test_image.jpg")
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        new_image = Image.query.filter_by(url=upload_path).first()
        self.assertIsNotNone(new_image)
        self.assertEqual(new_image.url, upload_path)

    def test_post_new_image_failure(self):
        payload = {
            'file': (BytesIO(b'test'), ''),
        }

        response = self.client.post('/images', data=payload, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)

    def test_get_images_success(self):
        response = self.client.get('/images')
        self.assertEqual(response.status_code, 200)

    def test_post_annotations_success(self):
        image = Image(url='test_fk.jbg')
        db.session.add(image)
        db.session.commit()
        image_id=image.id

        test_points = [[10,10],[20,30],[30,15]]

        payload = [
            {
                'type': 'box',
                'x': 10,
                'y': 10,
                'w': 10,
                'h': 10,
                'description': 'description',
            },
            {
                'type': 'polygon',
                'points': test_points,
                'description': 'description',
            }
        ]

        response = self.client.post(f'/images/{image_id}/annotations', data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 201)

        new_box = Box.query.filter(Box.image_id==image_id, Box.x_point==10, Box.y_point==10,
                                       Box.width==10, Box.height==10).first()
        self.assertIsNotNone(new_box)
        self.assertEqual(new_box.x_point, 10)
        self.assertEqual(new_box.y_point, 10)
        self.assertEqual(new_box.width, 10)
        self.assertEqual(new_box.height, 10)


        for index, point  in enumerate(test_points):
            new_polygon = Polygon.query.filter(Polygon.image_id == image_id,
                                        Point.x_point == point[0],
                                        Point.y_point == point[1],
                                        ).join(Image).join(Point).first()

            points = new_polygon.points
            self.assertIsNotNone(new_polygon)
            self.assertEqual(points[index].x_point, point[0])
            self.assertEqual(points[index].y_point, point[1])


    def test_post_annotations_failure(self):
        image = Image(url='test2_fk.jbg')
        db.session.add(image)
        db.session.commit()
        image_id = image.id

        test_points = [[10, 10], [20, 30], [30, 15]]

        payload = [
            {
                'type': 'undefined',
                'x': 10,
                'y': 10,
                'w': 10,
                'h': 10,
                'description': 'description',
            },
            {
                'type': 'polygon',
                'points': test_points,
                'description': 'description',
            }
        ]

        response = self.client.post(f'/images/{image_id}/annotations', data=json.dumps(payload),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)


    def test_get_annotations_success(self):
        image = Image(url='test3_fk.jbg')
        db.session.add(image)
        db.session.commit()
        image_id = image.id

        response = self.client.get(f'/images/{image_id}/annotations')

        self.assertEqual(response.status_code, 200)

    def test_get_annotations_failure(self):
        response = self.client.get(f'/images/1000/annotations')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Image not found", (json.loads(response.data))["error"])
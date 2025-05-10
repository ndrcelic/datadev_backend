from .image import ImageResource
from flask_restful import Api

def register_routes(app):
    api = Api(app)
    api.add_resource(ImageResource, '/image')
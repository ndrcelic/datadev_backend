from .image import ImageResource, ImageAnnotationResource,DownloadAnnotationsResource
from flask_restful import Api

def register_routes(app):
    api = Api(app)
    api.add_resource(ImageResource, '/images')
    api.add_resource(ImageAnnotationResource, '/images/<int:image_id>/annotations')
    api.add_resource(DownloadAnnotationsResource, '/images/<int:image_id>/download_annotations')
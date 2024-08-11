from flask import Flask
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os
from website.my_celery import make_celery

photos = UploadSet('photos', IMAGES)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sanmiareoye'
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.path.dirname(os.getcwd()), 'Femme', 'Barbershop', 'unprocessed')
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

    configure_uploads(app, photos)

    celery = make_celery()
    app.celery = celery

    with app.app_context():
        from .views import views
        app.register_blueprint(views)

    return app, celery

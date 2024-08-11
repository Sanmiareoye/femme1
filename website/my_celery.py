# my_celery.py
from celery import Celery

def make_celery():
    celery = Celery(__name__, backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')
    return celery

import os
import time
import exquiro
from celery import Celery
import requests


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="add_to_db_async")
def add_to_db_async(repo, owner):
    result = exquiro.create_app().add_models_from_github(repo_url=repo, owner=owner)
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'models_recognized': result[1],
            'models_added': result[0]}


@celery.task(name="delete_from_db_async")
def delete_from_db_async(repo, owner):
    result = exquiro.create_app().delete_models_from_github(repo_url=repo, owner=owner)
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'models_recognized': result[1],
            'models_deleted': result[0]}

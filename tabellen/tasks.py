import requests

from .config import celery


@celery.task
def test(url):
    return requests.post(url, json={"message": "This is a test"})

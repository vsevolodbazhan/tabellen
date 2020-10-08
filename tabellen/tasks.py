from requests import post as post_request, Response

from .config import celery

__all__ = ["Response", "post_request"]


@celery.task
def send_request(url, payload) -> Response:
    return post_request(url, json=payload)

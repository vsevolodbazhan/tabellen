from requests import Response
from requests import post as post_request

from .config import celery

__all__ = ["Response", "post_request", "revoke_task"]


@celery.task
def send_request(url, payload) -> Response:
    return post_request(url, json=payload)


def revoke_task(task_id: str) -> None:
    celery.control.revoke(task_id)

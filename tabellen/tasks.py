from typing import Any, Dict

from requests import Response
from requests import post as post_request

from .config import celery

__all__ = ["Response", "post_request", "revoke_task"]


@celery.task
def send_request(url: str, payload: Dict[str, Any]) -> Response:
    """A Celery task that sends a POST request to the given URL.

    Args:
        url (str): URL to send request to.
        payload (Dict[str, Any]): Request payload. Must be JSON-serializable.

    Returns:
        Response: Received response.
    """

    return post_request(url, json=payload)


def revoke_task(task_id: str) -> None:
    """Cancel a planned task.

    Args:
        task_id (str): Task ID.

    Returns:
        None
    """

    celery.control.revoke(task_id)

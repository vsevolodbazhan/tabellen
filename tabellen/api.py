from connexion import NoContent
from http import HTTPStatus

from .hooks import decode_callback_url


def hello():
    return {"message": "Hello!"}


def subscribe(body):
    tomoru_callback_url = body["tomoruCallbackUrl"]

    hook = decode_callback_url(url=tomoru_callback_url)
    hook.save()

    return NoContent, HTTPStatus.OK

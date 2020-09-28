from http import HTTPStatus

from connexion import NoContent

from .clients import extract_clients
from .event import Event
from .hooks import Hook, decode_callback_url


def send_message(body):
    bot_id, spreadsheet_id, column, range_start, range_end = (
        body["botId"],
        body["config"]["spreadsheetId"],
        body["config"]["column"],
        body["config"]["rangeStart"],
        body["config"]["rangeEnd"],
    )

    url = Hook.find_url_by_bot(bot=bot_id)
    if url is None:
        return NoContent, HTTPStatus.FAILED_DEPENDENCY

    event_type = "newMessage"
    clients = extract_clients(
        spreadsheet_id=spreadsheet_id,
        column=column,
        range_start=range_start,
        range_end=range_end,
    )
    for client in clients:
        event = Event(_type=event_type, client=client)
        event.send()

    return NoContent, HTTPStatus.OK


def subscribe(body):
    tomoru_callback_url = body["tomoruCallbackUrl"]

    hook = decode_callback_url(url=tomoru_callback_url)
    hook.save()

    return NoContent, HTTPStatus.OK

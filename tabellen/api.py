from http import HTTPStatus

from connexion import NoContent

from .clients import extract_clients
from .events import Event
from .hooks import Hook, decode_callback_url
from .sheets import retrieve_id


def send_message(body):
    bot_id, spreadsheet_url, column, range_start, range_end, message = (
        body["botId"],
        body["config"]["spreadsheetUrl"],
        body["config"]["column"],
        body["config"]["rangeStart"],
        body["config"]["rangeEnd"],
        body["config"]["message"],
    )
    spreadsheet_id = retrieve_id(url=spreadsheet_url)

    url = Hook.find_url_by_bot(bot=bot_id)
    if url is None:
        return NoContent, HTTPStatus.FAILED_DEPENDENCY

    event_type = "newMessage"
    event_data = {"message": message}
    clients = extract_clients(
        spreadsheet_id=spreadsheet_id,
        column=column,
        range_start=range_start,
        range_end=range_end,
    )
    for client in clients:
        event = Event(_type=event_type, data=event_data, client=client)
        event.send(url=url)

    return NoContent, HTTPStatus.OK


def subscribe(body):
    tomoru_callback_url = body["tomoruCallbackUrl"]

    hook = decode_callback_url(url=tomoru_callback_url)
    hook.save()

    return NoContent, HTTPStatus.OK

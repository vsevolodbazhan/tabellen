from http import HTTPStatus

from connexion import NoContent

from .clients import Client, extract_clients
from .events import Event
from .hooks import Hook, decode_callback_url
from .sheets import retrieve_id

__all__ = ["send_now", "subscribe"]

SECONDS_IN_MINUTE = 60


def send_now(body):
    bot_id, spreadsheet_url, column, range_start, range_end = (
        body["botId"],
        body["config"]["spreadsheetUrl"],
        body["config"]["column"],
        body["config"]["rangeStart"],
        body["config"]["rangeEnd"],
    )
    spreadsheet_id = retrieve_id(url=spreadsheet_url)

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
        event.send(url=url)

    return NoContent, HTTPStatus.OK


def send_later(body):
    bot_id, chat_id, message, delay = (
        body["botId"],
        body["chatId"],
        body["message"],
        body["delay"],
    )

    url = Hook.find_url_by_bot(bot=bot_id)
    if url is None:
        return NoContent, HTTPStatus.FAILED_DEPENDENCY

    client = Client(bot=bot_id, chat=chat_id)
    event_type = "newMessage"
    event = Event(_type=event_type, client=client, data={"message": message})
    event.send(url, delay * SECONDS_IN_MINUTE)

    return NoContent, HTTPStatus.OK


def subscribe(body):
    tomoru_callback_url = body["tomoruCallbackUrl"]

    hook = decode_callback_url(url=tomoru_callback_url)
    hook.save()

    return NoContent, HTTPStatus.OK

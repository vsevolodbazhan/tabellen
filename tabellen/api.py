from http import HTTPStatus

from connexion import NoContent

from .clients import Client, extract_clients
from .events import Event
from .hooks import Hook, decode_callback_url
from .sheets import retrieve_id
from .tasks import revoke_task

__all__ = ["send_now", "send_later", "cancel_event", "subscribe"]

SECONDS_IN_MINUTE = 60
NEW_MESSAGE_EVENT_TYPE = "newMessage"


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
    clients = extract_clients(
        spreadsheet_id=spreadsheet_id,
        column=column,
        range_start=range_start,
        range_end=range_end,
    )
    for client in clients:
        event = Event(_type=NEW_MESSAGE_EVENT_TYPE, client=client)
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
    client = Client(bot=bot_id, chat=chat_id)
    event = Event(
        _type=NEW_MESSAGE_EVENT_TYPE, client=client, data={"message": message}
    )
    message_id = event.send(url, delay * SECONDS_IN_MINUTE)

    return {"messageId": message_id}, HTTPStatus.OK


def cancel_event(body):
    message_id = body["messageId"]

    revoke_task(message_id)

    return NoContent, HTTPStatus.NO_CONTENT


def subscribe(body):
    tomoru_callback_url = body["tomoruCallbackUrl"]

    hook = decode_callback_url(url=tomoru_callback_url)
    hook.save()

    return NoContent, HTTPStatus.OK

from typing import Dict

import requests

from .client import Client

__all__ = ["send_event"]


def build_event_payload(event_type: str, client: Client) -> Dict[str, str]:
    """Build a payload for Tomoru event.

    Build a payload compatible with `TomoruEvent` schema.
    Schema: https://api.tomoru.ru/openapi#/components/schemas/TomoruEvent.

    Args:
        event_type (str): A type of an event.
        client (Client): A client an event will be sent to.

    Returns:
        Dict[str, str]: The JSON payload in a form of a Python's `dict`.

    Examples:
        >>> event_type = 'newMessage'
        >>> client = Client('abc123', 'cde456')
        >>> build_event_payload(event_type, client)
        {'event': 'newMessage', 'botId': 'abc123', 'chatUri': 'id://cde456'}
    """

    return {
        "event": event_type,
        "botId": client.bot,
        "chatUri": f"id://{client.chat}",
    }


def send_event(event_type: str, target: str, client: Client) -> None:
    """Send event to the given target URL.

    Args:
        event_type (str): A type of an event.
        target (str): A URL an event will be sent to.
        client (Client): A client an event will be sent to.

    Returns:
        None
    """

    payload = build_event_payload(event_type, client)
    requests.post(target, json=payload)

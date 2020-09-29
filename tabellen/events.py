from dataclasses import dataclass
from typing import Any, Dict

import requests

from .clients import Client

__all__ = ["Event"]


@dataclass
class Event:
    """An event that is being sent to Tomoru.

    Attributes:
        _type (str): An event type.
        data (Dict[str, Any]): An event data.
        client (Client): A Tomoru client.

    Examples:
        >>> client = Client(bot='abc123', chat='cde456')
        >>> event = Event(_type='newMessage', data={'message': 'Hello'}, client=client)
        >>> event._type
        'newMessage'
        >>> event.data
        {'message': 'Hello'}
        >>> event.client
        Client(bot='abc123', chat='cde456')
    """

    _type: str
    data: Dict[str, Any]
    client: Client

    @property
    def payload(self) -> Dict[str, Any]:
        """Build a payload for Tomoru event.

        Build a payload compatible with `TomoruEvent` schema.
        Schema: https://api.tomoru.ru/openapi#/components/schemas/TomoruEvent.

        Returns:
            Dict[str, str]: The JSON payload in a form of a Python's `dict`.

        Examples:
            >>> data = {'message': 'Hello'}
            >>> client = Client(bot='abc123', chat='cde456')
            >>> event = Event(_type='newMessage', data=data, client=client)
            >>> payload = event.payload
            >>> payload['event']
            'newMessage'
            >>> payload['botId']
            'abc123'
            >>> payload['chatUri']
            'id://cde456'
            >>> payload['data']
            {'message': 'Hello'}
        """

        return {
            "event": self._type,
            "botId": self.client.bot,
            "chatUri": f"id://{self.client.chat}",
            "data": {**self.data},
        }

    def send(self, url: str) -> None:
        """Send event to the given target URL.

        Args:
            url (str): A URL an event will be sent to.

        Returns:
            None
        """

        requests.post(url, json=self.payload)

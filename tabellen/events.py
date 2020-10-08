from dataclasses import dataclass
from typing import Any, Dict

from .clients import Client
from .tasks import Response, send_request

__all__ = ["Event"]


@dataclass
class Event:
    """An event that is being sent to Tomoru.

    Attributes:
        _type (str): An event type.
        client (Client): A Tomoru client.
        data (Dict[str, Any]): An additional data that
        will be send with an event.

    Examples:
        >>> client = Client(bot='abc123', chat='cde456')
        >>> data = {'message': 'Hello!'}
        >>> event = Event(_type='newMessage', client=client, data=data)
        >>> event._type
        'newMessage'
        >>> event.client
        Client(bot='abc123', chat='cde456')
        >>> event.data
        {'message': 'Hello!'}
    """

    _type: str
    client: Client
    data: Dict[str, Any] = {}

    @property
    def payload(self) -> Dict[str, Any]:
        """Build a payload for Tomoru event.

        Build a payload compatible with `TomoruEvent` schema.
        Schema: https://api.tomoru.ru/openapi#/components/schemas/TomoruEvent.

        Returns:
            Dict[str, str]: The JSON payload in a form of a Python's `dict`.

        Examples:
            >>> client = Client(bot='abc123', chat='cde456')
            >>> data = {'message': 'Hello!'}
            >>> event = Event(_type='newMessage', client=client, data=data)
            >>> payload = event.payload
            >>> payload['event']
            'newMessage'
            >>> payload['botId']
            'abc123'
            >>> payload['chatUri']
            'id://cde456'
            >>> payload['data']
            {'message': 'Hello!'}
        """

        return {
            "event": self._type,
            "botId": self.client.bot,
            "chatUri": f"id://{self.client.chat}",
            "data": self.data,
        }

    def send(self, url: str, delay: int = 1) -> Response:
        """Send event to the given target URL.

        Args:
            url (str): A URL an event will be sent to.

        Returns:
            requests.Response
        """

        return send_request.apply_async((url, self.payload), countdown=delay)

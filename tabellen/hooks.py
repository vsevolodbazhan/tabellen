from dataclasses import asdict, dataclass
from typing import Optional

import jwt

from .storage import find, insert_or_replace

__all__ = ["Hook", "decode_callback_url"]

COLLECTION_NAME = "hooks"


@dataclass
class Hook:
    """A webhook to send events to.

    Attributes:
        bot (str): A bot ID.
        url (str): A webhook URL.

    Examples:
        >>> hook = Hook('abc123', 'https://example.com/abc123')
        >>> hook
        Hook(bot='abc123', url='https://example.com/abc123')
        >>> hook.bot
        'abc123'
        >>> hook.url
        'https://example.com/abc123'
    """

    bot: str
    url: str

    def save(self) -> None:
        """Save this webhook to the database.

        Returns:
            None
        """

        insert_or_replace(
            collection_name=COLLECTION_NAME,
            query={"bot": self.bot},
            replacement=asdict(self),
        )

    @staticmethod
    def find_url_by_bot(bot: str) -> Optional[str]:
        """Find callback URL by a bot ID.

        Args:
            bot (str): A bot ID.

        Returns:
            str: A callback URL.
            None: if no callback URL corresponds to the given bot ID.
        """

        if document := find(collection_name=COLLECTION_NAME, query={"bot": bot}):
            return document["url"]

        return None


def decode_callback_url(url: str, token_prefix: str = "microservice-event/") -> Hook:
    """Decode callback URL.

    Args:
        url (str): A callback URL.
        token_prefix (str): A prefix after which the JWT starts.

    Returns:
        Hook: The decoded hook.

    Examples:
        >>> callback_url = 'https://example.org/token/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMzQ1IiwiYm90SWQiOiJhYmMxMjMiLCJpYXQiOjEyMzQ1LCJleHAiOjY3ODkwfQ.Qw4rFcAGSna18FOSXbmWSuZrLlsVmZ826EEqQJf7Btc' # noqa: E501
        >>> hook = decode_callback_url(url=callback_url, token_prefix='token/')
        >>> hook.bot
        'abc123'
        >>> hook.url == callback_url
        True
    """

    start = url.find(token_prefix)
    if start == -1:
        raise ValueError(
            f"Token prefix ({token_prefix}) wasn't found in the callback URL ({url})"
        )

    start += len(token_prefix)
    token = url[start:]
    payload = jwt.decode(token, verify=False)

    return Hook(bot=payload["botId"], url=url)

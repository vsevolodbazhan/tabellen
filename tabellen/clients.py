from dataclasses import dataclass
from typing import List

from .sheets import extract_values
from .utils import read_between

__all__ = ["Client", "extract_clients"]


@dataclass
class Client:
    """A client of a Tomoru bot.

    A client of a Tomoru bot described by a bot ID and a chat ID.

    Attributes:
        bot (str): A bot ID.
        chat (int): A chat ID.

    Examples:
        >>> client = Client('abc123', 'cde456')
        >>> client
        Client(bot='abc123', chat='cde456')
        >>> client.bot
        'abc123'
        >>> client.chat
        'cde456'
    """

    bot: str
    chat: str


def retrieve_bot(value: str) -> str:
    """Retrieve a bot ID from a string.

    Retrieve a bot ID between 'bot/' and '/chats' from a string.

    Args:
        value (str): A string that a bot ID is retrieved from.

    Returns:
        str: The retrieved bot ID.

    Raises:
        ValueError: If bot ID could not be retrieved.

    Examples:
        >>> retrieve_bot('bot/abc/chats')
        'abc'
        >>> retrieve_bot('abc/chats')
        Traceback (most recent call last):
            ...
        ValueError: Could not retrieve a bot ID from: abc/chats
        >>> retrieve_bot('bot/abc')
        Traceback (most recent call last):
            ...
        ValueError: Could not retrieve a bot ID from: bot/abc
    """

    prefix, postfix = "bot/", "/chats"
    if bot := read_between(value=value, prefix=prefix, postfix=postfix):
        return bot
    raise ValueError(f"Could not retrieve a bot ID from: {value}")


def retrieve_chat(value: str) -> str:
    """Retrieve a chat ID from a string.

    Retrieve a chat ID between 'chats/' and '";' from a string.

    Args:
        value (str): A string that a chat ID is retrieved from.

    Returns:
        str: The retrieved chat ID.

    Raises:
        ValueError: If chat ID could not be retrieved.

    Examples:
        >>> retrieve_chat('chats/abc";')
        'abc'
        >>> retrieve_chat('chats/abc')
        Traceback (most recent call last):
            ...
        ValueError: Could not retrieve a chat ID from: chats/abc
        >>> retrieve_chat('/abc";')
        Traceback (most recent call last):
            ...
        ValueError: Could not retrieve a chat ID from: /abc";
    """

    prefix, postfix = "chats/", '";'
    if chat := read_between(value=value, prefix=prefix, postfix=postfix):
        return chat
    raise ValueError(f"Could not retrieve a chat ID from: {value}")


def extract_clients(
    spreadsheet_id: str,
    column: str,
    range_start: int,
    range_end: int,
) -> List[Client]:
    """
    Extract clients from a spreadsheet.

    Extract clients described by a bot ID and a chat ID from a spreadsheet.
    Clients must be stored as hyperlinks.
    For example: =HYPERLINK("https://app.tomoru.ru/bot/abc123/chats/cde456"; "John Doe")

    Args:
        spreadsheet_id (str): An ID of a Google Spreadsheet.
        column (str): A spreadsheet column. For example, 'A' or 'AZ'.
        range_start (int): An upper bound of the extraction range.
        range_end (int): A lower bound of the extraction range.

    Returns:
        List[Client]: The list of extracted clients.
    """

    clients = []
    values = extract_values(
        spreadsheet_id=spreadsheet_id,
        column=column,
        range_start=range_start,
        range_end=range_end,
        render_option="FORMULA",
    )

    for value in values:
        client = Client(bot=retrieve_bot(value), chat=retrieve_chat(value))
        clients.append(client)

    return clients

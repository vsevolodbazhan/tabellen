import json
from typing import List

import googleapiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

from .settings import settings
from .utils import read_between

__all__ = ["extract_values"]


def setup_service(credentials_file: str = settings.SHEETS_CREDENTIALS_FILE):
    """Setup a Google Shreadsheets service.

    Args:
        credentials_file (str): A name of a file containing access credentials
        for Google Sheets API.

    Returns:
        Resourse: An authorized service instance.
    """

    apis_list = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file, apis_list
        )
    except FileNotFoundError:
        credentials_data = json.loads(settings.SHEETS_CREDENTIALS_JSON)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            credentials_data, apis_list
        )
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build("sheets", "v4", http=httpAuth)
    return service


def extract_values(
    spreadsheet_id: str,
    column: str,
    range_start: int,
    range_end: int,
    render_option: str,
) -> List[str]:
    """Extract values from a spreadsheet.

    Extract values from a spreadsheet column within given range.

    Args:
        spreadsheet_id (str): An ID of a Google Spreadsheet.
        column (str): A spreadsheet column. For example, 'A' or 'AZ'.
        range_start (int): An upper bound of the extraction range.
        range_end (int): A lower bound of the extraction range.
        render_option (str): A value rander option.
        Must be one of the following: 'FORMATTED_VALUE', 'UNFORMATTED_VALUE', 'FORMULA'.

    Returns:
        List[str]: A list of extracted values.
    """

    service = setup_service()
    data = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=f"{column}{range_start}:{column}{range_end}",
            majorDimension="COLUMNS",
            valueRenderOption=render_option,
        )
    ).execute()

    values = data.get("values")
    return values[0]


def retrieve_id(url: str, prefix: str = "d/", postfix: str = "/edit") -> str:
    """Get the spreadsheet ID from its URL.

    Parse the Google Spreadsheet URL and get
    the spreadsheet ID.

    Args:
        url (str): The spreadsheet URL.
        prefix (str): A prefix after which an ID starts.
        postfix (str): A postfix before which an ID.

    Returns:
        str: The retireved ID.

    Raises:
        ValueError: If an ID could not be retrieved.

    Examples:
        >>> url = 'https://docs.google.com/spreadsheets/d/abc123/edit?usp=sharing'
        >>> retrieve_id(url)
        'abc123'
        >>> url = 'some_random_string'
        >>> retrieve_id(url)
        Traceback (most recent call last):
            ...
        ValueError: Could not retrieve a spreadsheet ID from: some_random_string
    """

    if _id := read_between(value=url, prefix=prefix, postfix=postfix):
        return _id
    raise ValueError(f"Could not retrieve a spreadsheet ID from: {url}")

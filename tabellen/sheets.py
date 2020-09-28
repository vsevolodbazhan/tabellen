import json
import os
from typing import List

import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

__all__ = ["extract_values"]

CREDENTIALS_FILE = "credentials.json"
CREDENTIALS_NAME = "SHEETS_API_CREDS"


def setup_service(credentials_file: str = CREDENTIALS_FILE):
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
        credentials_data = json.loads(os.environ[CREDENTIALS_NAME])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            credentials_data, apis_list
        )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build("sheets", "v4", http=httpAuth)
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

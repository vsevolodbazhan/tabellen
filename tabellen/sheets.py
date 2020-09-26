from typing import List

import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

__all__ = ["extract_values"]

CREDENTIALS_FILE = "credentials.json"


def setup_service(credentials_file: str = CREDENTIALS_FILE):
    apis_list = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file, apis_list
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

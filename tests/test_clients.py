from tabellen.clients import Client, extract_clients
from tabellen.sheets import retrieve_id


def test_extract_clients(sheet_url):
    spreadsheet_id = retrieve_id(url=sheet_url)
    clients = extract_clients(
        spreadsheet_id=spreadsheet_id, column="A", range_start=2, range_end=3
    )

    assert clients == [
        Client(bot="abc123", chat="cde456"),
        Client(bot="efg789", chat="hij000"),
    ]

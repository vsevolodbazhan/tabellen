from tabellen.clients import Client, extract_clients
from tabellen.sheets import retrieve_id

TEST_SHEET_URL = "https://docs.google.com/spreadsheets/d/1dhFwVyDeJ5z7Hg0MPtusvcqWAlPZF82lw5g0MaW6YdY/edit?usp=sharing"  # noqa: E501


def test_extract_clients():
    spreadsheet_id = retrieve_id(url=TEST_SHEET_URL)
    clients = extract_clients(
        spreadsheet_id=spreadsheet_id, column="A", range_start=2, range_end=3
    )

    assert clients == [
        Client(bot="abc123", chat="cde456"),
        Client(bot="efg789", chat="hij000"),
    ]

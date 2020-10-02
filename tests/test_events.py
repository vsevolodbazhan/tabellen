import httpretty
from tabellen.clients import Client
from tabellen.events import Event


def test_send():
    httpretty.enable()
    url = "https://test.com"
    body = "Received event."
    httpretty.register_uri(httpretty.POST, url, body=body)

    client = Client(bot="abc123", chat="cde456")
    event = Event(_type="test", client=client)
    response = event.send(url=url)

    assert response.ok
    assert response.text == body

    httpretty.disable()
    httpretty.reset()

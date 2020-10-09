import httpretty
from tabellen.clients import Client
from tabellen.events import Event


def test_send():
    httpretty.enable()
    url = "https://test.com"
    body = "Received event."
    httpretty.register_uri(httpretty.POST, url, body=body)

    client = Client(bot="abc123", chat="cde456")
    data = {"message": "Hello!"}
    event = Event(_type="test", client=client, data=data)
    event_id = event.send(url=url)

    # Assert that `event.send` returns an ID of a Celery task.
    assert isinstance(event_id, str)
    assert len(event_id) == 36

    httpretty.disable()
    httpretty.reset()

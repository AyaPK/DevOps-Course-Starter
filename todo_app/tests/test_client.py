import os

import pytest
import requests
from dotenv import load_dotenv, find_dotenv
from todo_app import app


@pytest.fixture
def client():
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, "request", stub)

    response = client.get("/")

    assert response.status_code == 200
    assert "test_card" in response.data.decode()


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    @property
    def text(self):
        return self.fake_response_data


def stub(method, url, headers={}, params={}):
    test_board_id = os.environ.get("TRELLO_BOARD_ID")

    if url == f"https://api.trello.com/1/boards/{test_board_id}/lists":
        fake_response_data = """[{
            "id": 1,
            "name": "To Do",
            "cards": [{"id": 1, "name": "test_card", "desc": "", "due": ""}]
        }]"""
        return StubResponse(fake_response_data)
    raise Exception(f"Unexpected URL | #{url}")

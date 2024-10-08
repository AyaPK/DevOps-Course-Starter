import os
import pytest
import mongomock
from dotenv import load_dotenv, find_dotenv
from todo_app import app
from pymongo import MongoClient

@pytest.fixture
def client(monkeypatch):
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    mock_client = mongomock.MongoClient()
    monkeypatch.setattr(MongoClient, "__init__", lambda self, *args, **kwargs: None)
    monkeypatch.setattr(MongoClient, "get_database", lambda self, *args, **kwargs: mock_client['todo_app_db'])

    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client


def test_index_page(client):
    db = MongoClient().get_database("todo_app_db")  # The mocked database
    db.doing.insert_one({
        "id": 1,
        "name": "test_card",
        "desc": "",
        "due": "",
        "status": "To Do"
    })

    response = client.get("/")

    assert response.status_code == 200

import os

import pymongo
import pytest
import mongomock
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import pymongo


@pytest.fixture
def client(monkeypatch):
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    monkeypatch.setattr('pymongo.MongoClient', mongomock.MongoClient)

    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client


def test_index_page(client):
    MONGO_URI = os.getenv('MONGO_CONNECTION_STRING')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    db = pymongo.MongoClient(MONGO_URI).get_database(DATABASE_NAME)
    db.doing.insert_one({
        "id": 1,
        "name": "test_card",
        "desc": "",
        "due": "",
        "status": "To Do"
    })

    response = client.get("/")

    assert response.status_code == 200

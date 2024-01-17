from flask import session
import requests
import json
import os


class List:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.id})"


class Item:
    def __init__(self, id, name, idList):
        self.id = id
        self.name = name
        self.idList = idList
        self.list = get_list(self.idList)


def get_list(idList):
    url = f"https://api.trello.com/1/lists/{idList}"

    query = {
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN')
    }

    response = requests.request(
        "GET",
        url,
        params=query
    )
    result = json.loads(response.text)
    return List(result['id'], result['name'])


def get_all_cards():
    url = f"https://api.trello.com/1/boards/{os.getenv('TRELLO_BOARD_ID')}/cards"

    query = {
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN')
    }

    response = requests.request(
        "GET",
        url,
        params=query
    )
    result = json.loads(response.text)

    return [Item(item['id'], item['name'], item['idList']) for item in result]


def add_new_card(name):
    url = "https://api.trello.com/1/cards"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN'),
        'idList': os.getenv('TRELLO_NOT_STARTED_ID_LIST'),
        'name': name
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=query
    )
    return response.status_code


def delete_card(item_id):
    url = f"https://api.trello.com/1/cards/{item_id}"

    query = {
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN'),
    }

    response = requests.request(
        "DELETE",
        url,
        params=query
    )
    return response.status_code

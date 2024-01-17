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


def make_trello_request(endpoint, method="GET", params=None):
    url = f"https://api.trello.com/1/{endpoint}"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN'),
    }

    if params:
        query.update(params)


    print(query)
    print(url)
    response = requests.request(
        method,
        url,
        headers=headers,
        params=query
    )
    return response


def get_list(id_list):
    url = f"https://api.trello.com/1/lists/{id_list}"

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


def get_all_lists():
    endpoint = f"boards/{os.getenv('TRELLO_BOARD_ID')}/lists"
    response = make_trello_request(endpoint, method="GET")
    result = json.loads(response.text)
    return [List(l['id'], l['name']) for l in result]


def get_all_items():
    endpoint = f"boards/{os.getenv('TRELLO_BOARD_ID')}/cards"
    response = make_trello_request(endpoint, method="GET")

    result = json.loads(response.text)
    return [Item(item['id'], item['name'], item['idList']) for item in result]


def add_new_item(name):
    endpoint = "cards"
    params = {
        'idList': os.getenv('TRELLO_DEFAULT_LIST_ID'),
        'name': name
    }
    return make_trello_request(endpoint, method="POST", params=params).status_code


def delete_item(item_id):
    endpoint = f"cards/{item_id}"
    return make_trello_request(endpoint, method="DELETE").status_code


def move_item(item_id, list_id):
    endpoint = f"cards/{item_id}"
    params = {
        'idList': list_id
    }
    return make_trello_request(endpoint, method="PUT", params=params).status_code

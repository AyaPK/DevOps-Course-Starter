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

def get_all_lists():
    """
    Fetches all lists associated with the Trello  board

    Returns:
        array: An array of lists.
    """
    url = url = f"https://api.trello.com/1/boards/{os.getenv('TRELLO_BOARD_ID')}/lists"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN')
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )
    result = json.loads(response.text)
    print(result)
    return [List(item['id'], item['name']) for item in result]

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

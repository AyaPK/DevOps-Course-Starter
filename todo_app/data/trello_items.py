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
    """
    Method to make a Trello request

    Args:
        endpoint: The endpoint you would like to request
        method: The type of request, e.g. "GET", "PUT", "POST"
        params: A dict containing any additional parameters for the request

    Returns:
        A response object
    """
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

    response = requests.request(
        method,
        url,
        headers=headers,
        params=query
    )
    return response


def get_list(id_list):
    """
    Fetches the details of a single list

    Args:
        id_list: The ID of the list you would like to fetch

    Returns:
        A List object
    """
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
    """
    Fetches all lists on the board

    Returns:
        An array of List objects
    """
    endpoint = f"boards/{os.getenv('TRELLO_BOARD_ID')}/lists"
    response = make_trello_request(endpoint, method="GET")
    result = json.loads(response.text)
    return [List(l['id'], l['name']) for l in result]


def get_all_items():
    """
    Fetches all cards on the board

    Returns:
        An array of Item objects
    """
    endpoint = f"boards/{os.getenv('TRELLO_BOARD_ID')}/cards"
    response = make_trello_request(endpoint, method="GET")

    result = json.loads(response.text)
    return [Item(item['id'], item['name'], item['idList']) for item in result]


def add_new_item(name):
    """
    Adds a new item to the 'not-started' list

    Args:
        name: The name of the item

    Returns:
        The status code of the request as an integer
    """
    endpoint = "cards"
    params = {
        'idList': os.getenv('TRELLO_DEFAULT_LIST_ID'),
        'name': name
    }
    return make_trello_request(endpoint, method="POST", params=params).status_code


def delete_item(item_id):
    """
    Deletes an item from the board

    Args:
        item_id: The ID of the item to be deleted

    Returns:
        The status code of the request as an integer
    """
    endpoint = f"cards/{item_id}"
    return make_trello_request(endpoint, method="DELETE").status_code


def move_item(item_id, list_id):
    """
    Moves an item to a different list, changing its status

    Args:
        item_id: The ID of the item you'd like to move
        list_id: The ID of the target list

    Returns:
        The status code of the request as an integer
    """
    endpoint = f"cards/{item_id}"
    params = {
        'idList': list_id
    }
    return make_trello_request(endpoint, method="PUT", params=params).status_code

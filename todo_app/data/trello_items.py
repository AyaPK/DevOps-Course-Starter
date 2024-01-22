from datetime import datetime, date

from flask import session
import requests
import json
import os


class List:
    def __init__(self, id, name, items):
        self.id = id
        self.name = name
        self.items = []
        for item in items:
            self.items.append(Item.from_trello_response(item))

    @classmethod
    def from_trello_response(cls, response):
        return cls(response['id'], response['name'], response['cards'])


class Item:
    def __init__(self, id, name, desc, due=None):
        self.id = id
        self.name = name
        self.desc = desc

        if due:
            self.due = datetime.strptime(due, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        else:
            self.due = None

    def overdue(self):
        return date.today() > self.due if self.due else False

    def due_by_text(self):
        return f"Due by: {self.due}" if self.due else "No due date"

    @classmethod
    def from_trello_response(cls, response):
        return cls(response['id'], response['name'], response['desc'], response['due'])


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


def get_all_lists_and_items():
    """
    Gets all lists on the trello boards, as well as the items associated with them

    Returns:
        An array of List objects
    """
    endpoint = f"boards/{os.getenv('TRELLO_BOARD_ID')}/lists"
    params = {
        'cards': "open"
    }
    response = make_trello_request(endpoint, params=params, method="GET")
    result = json.loads(response.text)
    lists = [List.from_trello_response(lst) for lst in result]
    return lists


def add_new_item(name, desc, due):
    """
    Adds a new item to the 'not-started' list

    Args:
        name: The name of the item
        desc: The description of the item

    Returns:
        The status code of the request as an integer
    """
    endpoint = "cards"
    params = {
        'idList': os.getenv('TRELLO_DEFAULT_LIST_ID'),
        'name': name,
        'desc': desc,
        'due': due
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

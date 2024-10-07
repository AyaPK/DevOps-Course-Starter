from datetime import datetime, date

from flask import session
import requests
import json
import os
import pymongo
from bson.objectid import ObjectId

MONGO_URI = os.getenv('MONGO_CONNECTION_STRING')
DATABASE_NAME = os.getenv('DATABASE_NAME')

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
lists = ["to-do", "doing", "done"]
default_collection = db['to-do']


class List:
    def __init__(self, id, name, items):
        self.id = id
        self.name = name
        self.items = []
        for item in items:
            self.items.append(Item.from_mongo_response(item, self.id))

    @classmethod
    def from_mongo_response(cls, response):
        return cls(response['id'], response['name'], response['cards'])


class Item:
    def __init__(self, id, name, desc, list_id, due=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.list_id = list_id

        if due:
            self.due = datetime.strptime(due, "%Y-%m-%dT%H:%M:%S").date()
        else:
            self.due = None

    def overdue(self):
        return date.today() > self.due if self.due else False

    def due_by_text(self):
        return f"Due by: {self.due}" if self.due else "No due date"

    @classmethod
    def from_mongo_response(cls, response, list_id):
        return cls(response['_id'], response['name'], response['desc'], list_id, response['due'])


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


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
    Gets all lists and associated items from MongoDB.
    Returns:
        An array of List objects
    """
    collections_data = []
    for collection_name in db.list_collection_names():
        documents = list(db[collection_name].find({}))
        data = {
            "id": collection_name,
            "name": collection_name.capitalize(),
            "cards": [
                doc for doc in documents
            ]
        }
        collections_data.append(data)
    collections_json = json.loads(json.dumps(collections_data, indent=4, cls=MongoJSONEncoder))

    return [List.from_mongo_response(lst) for lst in collections_json]


def add_new_item(name, desc, due):
    """
    Adds a new item to a specific list in MongoDB.

    Args:
        name: The name of the item
        desc: The description of the item
        due: The due date for the item

    Returns:
        Whether the addition was successful (boolean)
    """
    due_date = datetime.strptime(due+"T00:00:00.000000Z", "%Y-%m-%dT%H:%M:%S.%fZ") if due else None
    new_item = {
        'name': name,
        'desc': desc,
        'due': due_date,
    }
    return True if default_collection.insert_one(new_item) else False


# def delete_item(item_id):
#     """
#     Deletes an item from the board
#
#     Args:
#         item_id: The ID of the item to be deleted
#
#     Returns:
#         The status code of the request as an integer
#     """
#     endpoint = f"cards/{item_id}"
#     return make_trello_request(endpoint, method="DELETE").status_code


def delete_item(item_id, list_name):
    """
    Deletes an item from MongoDB.

    Args:
        item_id: The ID of the item to be deleted
        list_name: The name of the list the item is in

    Returns:
        Whether the deletion was successful (boolean)
    """
    collection = db[list_name]
    result = collection.delete_one({'_id': ObjectId(item_id)})
    return result.deleted_count > 0


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

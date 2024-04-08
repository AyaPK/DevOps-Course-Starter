from todo_app.viewmodels import IndexViewModel
from todo_app.data.trello_items import Item, List

test_items = [
    {"id": 1, "name": "Task 1", "desc": "The first task", "due": ""},
    {"id": 1, "name": "Task 1", "desc": "The first task", "due": ""},
    {"id": 1, "name": "Task 1", "desc": "The first task", "due": ""},
    {"id": 1, "name": "Task 1", "desc": "The first task", "due": ""}
]


def test_viewmodel_todo_property():
    test_lists = [List(1, "To Do", test_items)]
    viewmodel = IndexViewModel(test_lists)

    assert len(viewmodel.done_items) == 4


def test_viewmodel_doing_property():
    test_lists = [List(1, "Doing", test_items)]
    viewmodel = IndexViewModel(test_lists)

    assert len(viewmodel.done_items) == 4


def test_viewmodel_done_property():
    test_lists = [List(1, "Done", test_items)]
    viewmodel = IndexViewModel(test_lists)

    assert len(viewmodel.done_items) == 4

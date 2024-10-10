from todo_app.viewmodels import IndexViewModel
from todo_app.data.mongo_items import Item, List

test_items = [
    {"_id": 1, "name": "Task 1", "desc": "The first task", "due": ""},
    {"_id": 2, "name": "Task 2", "desc": "The second task", "due": ""},
    {"_id": 3, "name": "Task 3", "desc": "The third task", "due": ""},
    {"_id": 4, "name": "Task 4", "desc": "The fourth task", "due": ""}
]

def test_viewmodel_todo_property():
    test_lists = [List("to-do", "To Do", test_items)]
    viewmodel = IndexViewModel(test_lists)

    assert len(viewmodel.to_do_items) == 4


def test_viewmodel_doing_property():
    test_lists = [List("doing", "Doing", test_items)]
    viewmodel = IndexViewModel(test_lists)

    assert len(viewmodel.doing) == 4


def test_viewmodel_done_property():
    test_lists = [List("done", "Done", test_items)]
    viewmodel = IndexViewModel(test_lists)

    assert len(viewmodel.done_items) == 4

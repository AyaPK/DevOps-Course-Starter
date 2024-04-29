import json
import os
from time import sleep
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from dotenv import load_dotenv
from todo_app import app
import pytest


@pytest.fixture(scope="module")
def app_with_temp_board():
    load_dotenv(override=True)
    board_id = create_trello_board()
    default_list_id = get_default_list(board_id)
    os.environ["TRELLO_BOARD_ID"] = board_id
    os.environ["TRELLO_DEFAULT_LIST_ID"] = default_list_id

    application = app.create_app()
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    sleep(1)

    yield application

    thread.join(1)
    delete_trello_board(board_id)


def create_trello_board():
    url = "https://api.trello.com/1/boards/"
    query = {
        'key': os.environ["TRELLO_API_KEY"],
        'token': os.environ["TRELLO_API_TOKEN"],
        'name': 'Test Board'
    }
    response = requests.post(url, params=query)
    if response.status_code == 200:
        return response.json()['url'].split("/b/")[1].split("/")[0]
    else:
        return None


def get_default_list(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    query = {
        'key': os.environ["TRELLO_API_KEY"],
        'token': os.environ["TRELLO_API_TOKEN"],
    }
    response = requests.get(url, params=query)
    if response.status_code == 200:
        return [l for l in response.json() if l['name'] == "To Do"][0]['id']
    else:
        print("Failed to delete board.")


def delete_trello_board(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}"
    query = {
        'key': os.environ["TRELLO_API_KEY"],
        'token': os.environ["TRELLO_API_TOKEN"],
    }
    response = requests.delete(url, params=query)
    if response.status_code == 200:
        print("Board deleted successfully.")
    else:
        print("Failed to delete board.")


def select_card(driver, card_name):
    return [card for card in driver.find_elements(By.CLASS_NAME, "card") if card_name in card.text][0]


@pytest.fixture(scope="module")
def driver():
    driver_options = Options()
    # driver_options.add_argument("--headless")
    # driver_options.add_argument("--disable-gpu")

    with webdriver.Chrome(options=driver_options) as driver:
        yield driver


def test_site_index_loads(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    assert driver.title == "To-Do App"
    assert "Just another to-do app." in driver.page_source


def test_end_to_end(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    driver.find_element(By.NAME, "name").send_keys("A new task")
    driver.find_element(By.NAME, "desc").send_keys("A new task's description")
    driver.find_element(By.ID, "add-task-btn").click()
    assert driver.title == "To-Do App"
    assert "A new task's description" in driver.find_element(By.ID, "to-do-tasks").text


def test_move_task_to_doing(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    driver.find_element(By.NAME, "name").send_keys("An in progress task")
    driver.find_element(By.NAME, "desc").send_keys("An in progress task's description")
    driver.find_element(By.ID, "add-task-btn").click()
    assert driver.title == "To-Do App"
    assert "An in progress task's description" in driver.find_element(By.ID, "to-do-tasks").text

    card = select_card(driver, "An in progress task")
    selector = Select(card.find_element(By.ID, "dropdown-status-selection"))
    selector.select_by_visible_text("Doing")
    card.find_element(By.ID, "update-task-button").click()

    assert "An in progress task's description" in driver.find_element(By.ID, "doing-tasks").text


def test_delete_a_task(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    driver.find_element(By.NAME, "name").send_keys("A task to be deleted")
    driver.find_element(By.NAME, "desc").send_keys("A deletable task's description")
    driver.find_element(By.ID, "add-task-btn").click()
    assert driver.title == "To-Do App"
    assert "A deletable task's description" in driver.find_element(By.ID, "to-do-tasks").text

    card = select_card(driver, "A task to be deleted")
    card.find_element(By.ID, "delete-task-btn").click()
    assert "A deletable task's description" not in driver.find_element(By.ID, "to-do-tasks").text
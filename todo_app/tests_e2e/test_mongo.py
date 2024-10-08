import json
import os
from time import sleep
from threading import Thread

import pymongo
from bson import ObjectId
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from dotenv import load_dotenv
from todo_app import app
import pytest


@pytest.fixture(scope="module")
def app_with_temp_board():
    load_dotenv(override=True)
    client = pymongo.MongoClient("mongodb://mongodb:27017")
    db = client["to_do_test"]
    lists = ["to-do", "doing", "done"]
    default_collection = db['to-do']
    for lst in lists:
        collection = db[lst]
        temp_item = collection.insert_one({})
        collection.delete_one({'_id': ObjectId(temp_item.inserted_id)})

    application = app.create_app()
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    sleep(1)

    yield application

    thread.join(1)
    client.drop_database(db)


def select_card(driver, card_name):
    return [card for card in driver.find_elements(By.CLASS_NAME, "card") if card_name in card.text][0]


@pytest.fixture(scope="module")
def driver():
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--no-sandbox")
    driver_options.add_argument("--disable-dev-shm-usage")
    driver_options.add_argument("--disable-gpu")

    service = Service(executable_path='/usr/local/bin/chromedriver')

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
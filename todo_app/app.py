from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item
from todo_app.data.trello_items import get_all_items, add_new_item, delete_item, get_all_lists, move_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_all_items(), lists=get_all_lists())


@app.route('/item', methods=['POST'])
def add_created_item():
    if add_new_item(request.form.get('name'), request.form.get('desc'), request.form.get('due-date')) == 200:
        return redirect('/')
    else:
        # Handle the error
        pass


@app.route("/delete_item", methods=['POST'])
def delete_selected_item():
    if delete_item(request.form.get('item-id')) == 200:
        return redirect('/')
    else:
        # Handle the error
        pass


@app.route("/move_item", methods=['POST'])
def move_item_to_new_list():
    if move_item(request.form.get('item-id'), request.form.get('list-id')) == 200:
        return redirect('/')
    else:
        # Handle the error
        pass

from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item
from todo_app.data.trello_items import get_all_cards, add_new_card, delete_card

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_all_cards())


@app.route('/item', methods=['POST'])
def add_new_item():
    if add_new_card(request.form.get('name')) == 200:
        return redirect('/')
    else:
        # Do something with the error
        pass


@app.route("/delete_item", methods=['POST'])
def delete_item():
    if delete_card(request.form.get('item-id')) == 200:
        return redirect('/')
    else:
        # Handle the error
        pass

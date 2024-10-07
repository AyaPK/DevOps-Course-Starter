from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.data.trello_items import add_new_item, delete_item, move_item, get_all_lists_and_items
from todo_app.viewmodels import IndexViewModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        return render_template('index.html', view_model=(IndexViewModel(get_all_lists_and_items())))

    @app.route('/item', methods=['POST'])
    def add_created_item():
        if add_new_item(request.form.get('name'), request.form.get('desc'), request.form.get('due-date')):
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

    return app

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from todo_app.flask_config import Config
from todo_app.data.mongo_items import init_db, add_new_item, delete_item, move_item, get_all_lists_and_items
from todo_app.viewmodels import IndexViewModel
from todo_app.oauth import blueprint, login_required
from flask_dance.contrib.github import github


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config())
    init_db()

    app.register_blueprint(blueprint, url_prefix="/login")

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html', view_model=(IndexViewModel(get_all_lists_and_items())))

    @app.route('/item', methods=['POST'])
    @login_required
    def add_created_item():
        if add_new_item(request.form.get('name'), request.form.get('desc'), request.form.get('due-date')):
            return redirect('/')
        else:
            # Handle the error
            pass

    @app.route("/delete_item", methods=['POST'])
    @login_required
    def delete_selected_item():
        if delete_item(request.form.get('item-id'), request.form.get('list-id')):
            return redirect('/')
        else:
            pass

    @app.route("/move_item", methods=['POST'])
    @login_required
    def move_item_to_new_list():
        if move_item(request.form.get('item-id'), request.form.get('current-list-id'), request.form.get('new-list-id')):
            return redirect('/')
        else:
            # Handle the error
            pass

    return app

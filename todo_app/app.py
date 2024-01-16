from flask import Flask, render_template, request
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_items())

@app.route('/item', methods=['POST'])
def add_new_item():
    add_item(request.form.get('name'))
    return render_template('index.html', items=get_items())
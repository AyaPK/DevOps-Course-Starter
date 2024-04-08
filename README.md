# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Adding environment variables

The app communicates with the Trello API to function, and so you will need to add some details to the .env file in order for it to work.

Create a Trello power-up to get an API key and Token, these can be easily obtained by following the [Trello API docs](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#managing-your-api-key).

Once you have your API Key and Token, and them to your environment variables under `TRELLO_API_KEY` and `TRELLO_API_TOKEN`

Finally, you will need to make a Trello Board with at least one List. Once you have created them, add the ID for both the Board and the List to the environment variables under `TRELLO_BOARD_ID` and `TRELLO_DEFAULT_LIST_ID`.
(As the name suggests, this list is the default location for newly made items).

## Setting up Trello

Your Trello board is expected to have at least three lists, named `To Do`, `Doing`, and `Done`, where the `To Do` list is used to populate the above `TRELLO_DEFAULT_LIST_ID`.

Further columns may be added, and can/should work, but are not officially supported.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running Tests

To run the full test suite, execute the `pytest` command from the project root.

You can run an individual set of tests by passing the test directory as an argument. E.g.
```bash
$ pytest todo_app\test_client.py 
```
or
```bash
$ pytest todo_app\test_viewmodel.py 
```

Additionally, you can run a single test with the `<test_directory>::<test_name>` argmuent. E.g.
```bash
$ pytest todo_app\test_viewmodel.py::test_viewmodel_todo_property
```
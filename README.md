# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

### This project uses Docker for local development, ensure you have Docker installed before continuing.

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

## Running the App

Once all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ docker compose up development
```

Docker will set up your development container, and you should see output similar to the following:
```bash
Attaching to development-1
development-1  |  * Serving Flask app 'todo_app/app'
development-1  |  * Debug mode: on
development-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.                                                                                                                                                                                 
development-1  |  * Running on all addresses (0.0.0.0)
development-1  |  * Running on http://127.0.0.1:5000                                                                                                                                                                                                                                                                    
development-1  |  * Running on http://172.18.0.3:5000                                                                                                                                                                                                                                                                   
development-1  | Press CTRL+C to quit                                                                                                                                                                                                                                                                                   
development-1  |  * Restarting with stat                                                                                                                                                                                                                                                                                
development-1  |  * Debugger is active!                                                                                                                                                                                                                                                                                 
development-1  |  * Debugger PIN: 214-115-548
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running Tests
Selenium tests run using a Chrome headless browser. Chrome may need to be installed on your system for these tests to work.

To run the full test suite, execute the `poetry run pytest` command from the project root.

You can run an individual set of tests by passing the test directory as an argument. E.g.
```bash
$ poetry run pytest todo_app\tests
```
or
```bash
$ poetry run pytest todo_app\tests_e2e\test_mongo.py 
```

Additionally, you can run a single test with the `<test_directory>::<test_name>` argument. E.g.
```bash
$ poetry run pytest todo_app\tests\test_viewmodel.py::test_viewmodel_todo_property
```

## Deploying the app

### This app is deployed using an ansible playbook.

To deploy the app, first have at least two linux hosts available, a control node and at least one host.

With ansible installed on the control node, copy the contents of the ansible folder to the control node, ensuring you update `inventory.yml` to use the host's IP.

Connect to the control node and run
```bash
$ ansible-playbook playbook.yml -i inventory.yml
```
in the directory containing the ansible files, providing the `trello_api_key` and `trello_api_token` when prompted.

Visit `http://your.server.ip.address:5000` to view the deployed application.

## Running in Docker

With Docker Desktop installed, run one of the following commands from the project root:

Running in dev:
```bash
$ docker compose up development
```

Running in prod:
```bash
$ docker compose up production
```

You may also run the test suite within Docker:
```bash
$ docker compose up test
```
You can find the latest version of the Docker image on [DockerHub](https://hub.docker.com/repository/docker/ayastead/todoapp/general)

## MongoDB setup

This app uses MongoDB to persist data storage.
When developing locally, Docker will handle the database, but running in production will require a database set up.

With a Mongo database set up, ensure that the following environment variables exist when deploying:
- `MONGO_CONNECTION_STRING`: The connection string for your MongoDB
- `DATABASE_NAME`: The name of the database to be used (It will be created if it doesn't exist)

## Deploying to Azure
The ToDo App can be deployed as an Azure WebApp by following the below steps.

1) Build the Docker Image (e.g.)
    ```bash
    $ docker build --target production -t ayastead/todoapp:todoapp .
    ```
2) Create an Azure WebApp, ensuring your Publish option is set to Docker Container, and contains the details to the above image
3) Ensure any enviroment variables are added to `settings` > `Environment Variables` on your Azure WebApp
4) Wait for the Docker Image to build and spin up

To manually trigger a redeployment, hit the webhook with a POST request (e.g.)
```bash
$ curl -v -X POST '<webhook URL>'
```
You can find the webhook URL in the WebApp's `Deployment Center`

## Live App
The Live App can be accessed via [The Deployed Azure Webapp](https://ayaste-todoapp-fmfzg2h2gbf9etd9.uksouth-01.azurewebsites.net).
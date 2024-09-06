FROM python:3.11-buster as base

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /todo_app
COPY pyproject.toml poetry.toml poetry.lock ./
RUN poetry install --no-root

EXPOSE 5000

FROM base as production
ENV FLASK_DEBUG=false
COPY . /todo_app
ENTRYPOINT poetry run gunicorn -b 0.0.0.0:5000 "todo_app.app:create_app()"

FROM base as development
ENV FLASK_DEBUG=true
COPY . /todo_app
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as test
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable
COPY . /todo_app
RUN poetry install
ENV PYTHONPATH=/todo_app:$PYTHONPATH
WORKDIR /todo_app
ENV DISPLAY=:99
ENTRYPOINT poetry run pytest

FROM python:3.11-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /todo_app
COPY . .

RUN poetry install --no-root

ENTRYPOINT poetry run gunicorn -b 0.0.0.0:5000 "todo_app.app:create_app()"
EXPOSE 5000

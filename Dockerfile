# Use Python 3.8 with Buster OS as base image
FROM python:3.8-buster

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Poetry dependencies
RUN poetry install --no-root --verbose

# Define the entrypoint and default command to run the application
ENTRYPOINT ["poetry", "run"]
CMD ["python", "app.py"]

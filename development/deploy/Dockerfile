# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 5000

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        postgresql-client \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the dependencies file to optimize caching
COPY poetry.lock pyproject.toml /app/

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the Flask port
EXPOSE $PORT

# Command to run the Flask application
CMD ["flask", "run", "--host 0.0.0.0", "--port $PORT"]

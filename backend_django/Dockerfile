FROM python:3.10.11-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /app

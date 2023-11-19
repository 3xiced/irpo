FROM --platform=linux/amd64 python:3.11-slim as builder

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /usr/src

COPY poetry.lock pyproject.toml /usr/src/

RUN pip3 install poetry

RUN poetry install --no-dev

FROM builder

WORKDIR /usr/src/app

COPY ./src /usr/src/app/src
COPY .env /usr/src/app/


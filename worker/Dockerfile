# Python version
ARG PYV=3.11

# It is assumed that there are only two groups
# of dependencies in `pyproject.toml`: `main` and `dev`.
# `BUILD_ENV` may be either `dev` or `production`
ARG BUILD_ENV=dev

# User on behalf of whom we run containers
ARG USER_NAME=docker
ARG USER_ID=1000


# ---------------
# FULL SIZE IMAGE
FROM python:${PYV} as build-python
MAINTAINER Titov Anton <webdev@titovanton.com>

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install poetry

ARG USER_NAME
ARG USER_ID
RUN groupadd -r $USER_NAME -g $USER_ID && \
    useradd -m -r -g $USER_NAME -u $USER_ID $USER_NAME && \
    echo "$USER_NAME:$USER_NAME" | chpasswd && \
    adduser $USER_NAME sudo

RUN poetry config virtualenvs.in-project false
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY ./ /app/

ARG BUILD_ENV
RUN poetry install \
    $(test "$BUILD_ENV" == "production" && echo "--no-dev") \
    --no-interaction

USER $USER_NAME


# ----------
# SLIM IMAGE

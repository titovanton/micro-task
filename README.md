# Task queue service

Recieves task name, adds to the queue, background tasks polling. Task status can be checked by task ID.

### Install

You must have Docker properly configured on your machine, please follow the documentation, also don't forget to create docker group and follow the prompts after the main install article.

Clone repo, create empty .env file in the root dir.

### Tests

    docker-compose run --rm worker pytest

### Running app

    docker-compose up -d

### API docs

    http://localhost:8000/docs

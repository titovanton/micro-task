from datetime import datetime, timedelta
from random import choice
from typing import Generator, Callable

import pytest
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from redis import StrictRedis
from uuid6 import uuid6

from worker.main import app as main_app
from worker.redis_connection import rcon as redis_con
from worker.schemas import Task, TaskStatus


fake = Faker()


@pytest.fixture
def rcon() -> Generator[StrictRedis, None, None]:
    yield redis_con
    redis_con.flushdb()


@pytest.fixture
def app() -> Generator[FastAPI, None, None]:
    yield main_app


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture
def create_task() -> Callable:
    def inner() -> Task:
        now = datetime.now()
        _exp_sec = choice(range(60, 3 * 60))
        exp_date = now + timedelta(seconds=_exp_sec)

        task = Task(
            id=uuid6(),
            title=fake.word(),
            expiration_date=exp_date,
            status=TaskStatus.WAITING
        )

        return task
    return inner

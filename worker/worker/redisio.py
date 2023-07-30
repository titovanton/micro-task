from collections import deque
from datetime import datetime, timedelta
from random import choice

from uuid6 import uuid6, UUID

from .log import log
from .redis_connection import rcon
from .schemas import Task, TaskStatus
from .settings import TASK_QUEUE


def get_task(task_id: UUID) -> Task | None:
    task_json = rcon.get(str(task_id))
    if task_json:
        return Task.parse_raw(task_json)
    return None


def save_task_obj(task: Task) -> None:
    """
    Adds key->value record to the DB,
    where key is task.id and value is task.json().
    """
    rcon.set(str(task.id), task.json())


def add_task_obj(task: Task) -> None:
    rcon.lpush(TASK_QUEUE, task.json())


def add_task(
    task_title: str,
    exp_sec: int | None = None
) -> UUID:
    """
    Creates task and adds task object to the queue and
    adds key->value record to the DB,
    where key is task.id and value is task.json().
    """

    id = uuid6()
    log.info(f'Adding task#"{id}" to the queue...')
    now = datetime.now()
    _exp_sec = exp_sec if exp_sec else choice(range(3 * 60))
    exp_date = now + timedelta(seconds=_exp_sec)
    task = Task(id=id, title=task_title, expiration_date=exp_date)

    add_task_obj(task)
    save_task_obj(task)

    return id


def poll_queue() -> None:
    """
    Iterates through the queue:
      - tasks which are done - go out from the queue
      - tasks which are in waiting - will be pushed
        to the queue again in same order
      - key-value records will be updated for
        tasks which are done.
    """

    queue: deque[Task] = deque()

    while task_json := rcon.rpop(TASK_QUEUE):
        task = Task.parse_raw(task_json)
        if task.expiration_date <= datetime.now():
            task.status = TaskStatus.DONE

            save_task_obj(task)

            log.info(f'Task#"{task.id}" is done!')
        else:
            queue.appendleft(task)

    while len(queue):
        task = queue.pop()

        add_task_obj(task)

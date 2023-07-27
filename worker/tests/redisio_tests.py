from datetime import datetime

from worker.redisio import get_task, save_task_obj, add_task_obj
from worker.redisio import add_task, poll_queue
from worker.schemas import Task, TaskStatus
from worker.settings import TASK_QUEUE


def test_get_task(create_task, rcon):
    task = create_task()
    rcon.set(str(task.id), task.model_dump_json())
    res = get_task(task.id)
    assert res.id == task.id

    rcon.delete(str(task.id))
    res = get_task(task.id)
    assert res is None


def test_save_task_obj(create_task):
    task = create_task()
    save_task_obj(task)
    assert task == get_task(task.id)


def test_add_task_obj(rcon, create_task):
    task1 = create_task()
    task2 = create_task()
    assert task1.id != task2.id

    add_task_obj(task1)
    add_task_obj(task2)

    task_json = rcon.rpop(TASK_QUEUE)
    task = Task.model_validate_json(task_json)
    assert task.id == task1.id

    task_json = rcon.rpop(TASK_QUEUE)
    task = Task.model_validate_json(task_json)
    assert task.id == task2.id


def test_add_task(rcon):
    id = add_task('word', 35)

    raw_json = rcon.get(str(id))
    task = Task.model_validate_json(raw_json)
    assert task.id == id
    raw_json = rcon.rpop(TASK_QUEUE)
    task = Task.model_validate_json(raw_json)
    assert task.id == id
    none = rcon.rpop(TASK_QUEUE)
    assert none is None


def test_poll_queue(create_task, rcon):
    task1 = create_task()
    task2 = create_task()
    assert task1.id != task2.id

    add_task_obj(task1)
    add_task_obj(task2)

    assert rcon.llen(TASK_QUEUE) == 2
    poll_queue()
    assert rcon.llen(TASK_QUEUE) == 2
    rcon.delete(TASK_QUEUE)

    task2.expiration_date = datetime.now()
    add_task_obj(task1)
    add_task_obj(task2)
    assert rcon.llen(TASK_QUEUE) == 2
    poll_queue()
    assert rcon.llen(TASK_QUEUE) == 1
    raw_json = rcon.rpop(TASK_QUEUE)
    task = Task.model_validate_json(raw_json)
    assert task.id == task1.id
    task = get_task(task2.id)
    assert task.status is TaskStatus.DONE
    assert rcon.llen(TASK_QUEUE) == 0

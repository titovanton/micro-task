import asyncio
from http import HTTPStatus
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from uuid6 import UUID

from .log import log
from .redisio import add_task, poll_queue, get_task


app = FastAPI()


StrOrNone = Annotated[
    str | None,
    Query(description='str or null')
]
IntOrNone = Annotated[
    int | None,
    Query(description='str or null')
]


async def background_broker():
    while True:
        log.info('Poll queue...')
        poll_queue()
        await asyncio.sleep(1)


@app.on_event('startup')
async def on_startup():
    asyncio.create_task(background_broker())


@app.post('/')
async def add_task_api(
    task_title: str,
    exp_sec: IntOrNone = None,
) -> dict:
    id = add_task(task_title, exp_sec)
    return {'task_id': id}


@app.get('/')
async def get_task_api(task_id: StrOrNone = None) -> dict:
    not_found = HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=f'Task#"{task_id}" not found!'
    )

    if not task_id:
        return {'message': 'Please specify GET parameter `task_id`'}

    try:
        id = UUID(task_id)
    except ValueError:
        raise not_found

    task = get_task(id)
    if not task:
        raise not_found

    return task.dict()

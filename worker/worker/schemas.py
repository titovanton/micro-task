import enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskStatus(str, enum.Enum):
    WAITING = 'waiting'
    DONE = 'done'


class Task(BaseModel):
    id: UUID
    title: str
    expiration_date: datetime
    status: TaskStatus = TaskStatus.WAITING

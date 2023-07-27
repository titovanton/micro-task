import enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .log import log


class TaskStatus(str, enum.Enum):
    WAITING = 'waiting'
    DONE = 'done'


class UUID6(UUID):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        log.debug(f'validate {value}')
        if not value:
            raise ValueError('Value cannot be empty')
        return cls(value)


class Task(BaseModel):
    id: UUID
    title: str
    expiration_date: datetime
    status: TaskStatus = TaskStatus.WAITING

    class Config:
        arbitrary_types_allowed = True

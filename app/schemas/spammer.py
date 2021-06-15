from typing import Any, List, Optional, Union
from pydantic import BaseModel, HttpUrl
from enum import Enum

from core.base_schemas import BaseResult


class SpammerStateEnum(str, Enum):
    working = 'working'
    stopped = 'stopped'


class SpammerResultEnum(str, Enum):
    success = 'success'
    database_err = 'database error'
    spammer_err = 'spammer process error'


class SpammerTarget(BaseModel):
    target_type: str
    current: int
    total: int


class SpammerBase(BaseModel):
    spammer_type: str
    login: str
    target: SpammerTarget
    state: SpammerStateEnum


class SpammerIn(SpammerBase):
    pass


class SpammerStore(SpammerBase):
    id: int

    class Config:
        orm_mode = True


class SpammerOut(SpammerStore):
    pass


class SpammerCommand(BaseModel):
    command: str
    data: Union[SpammerIn, List[SpammerIn], List[int]]


class SpammerResult(BaseResult):
    data: Union[List[SpammerOut], str]
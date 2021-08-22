from typing import Any, List, Optional, Union, Dict
from pydantic import BaseModel, HttpUrl, Json
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
    script_template: str
    login: str
    password: str
    state: SpammerStateEnum = SpammerStateEnum.stopped
    options: Dict = dict()


class SpammerIn(SpammerBase):
    pass


class SpammerStore(SpammerBase):
    id: int
    statistics: Dict = dict()

    class Config:
        orm_mode = True


class SpammerCommand(BaseModel):
    command: str
    data: Union[SpammerStore, List[SpammerStore], List[int]]


class BaseResult(BaseModel):
    status: str


class SpammerResult(BaseResult):
    data: SpammerStore


class SpammerListResult(BaseResult):
    data: List[SpammerStore]


class SpammerIdsResult(BaseResult):
    data: List[int]


class SpammerErrorResult(BaseResult):
    data: str

from pydantic import BaseModel, HttpUrl
from enum import Enum

class SpammerStateEnum(str, Enum):
    idle = 'idle'
    working = 'working'
    stopped = 'stopped'

class SpammerBase(BaseModel):
    name: str
    target: HttpUrl

class SpammerIn(SpammerBase):
    pass

class SpammerStore(SpammerBase):
    id: int

    class Config:
        orm_mode = True

class SpammerOut(SpammerStore):
    state: SpammerStateEnum = SpammerStateEnum.idle
    progress: int


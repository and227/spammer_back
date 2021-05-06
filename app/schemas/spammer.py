from pydantic import BaseModel, HttpUrl
from enum import Enum

class SpammerStateEnum(str, Enum):
    idle = 'idle'
    working = 'working'
    stopped = 'stopped'

class Spammer(BaseModel):
    id: int
    name: str
    target: HttpUrl
    state: SpammerStateEnum = SpammerStateEnum.idle
    progress: int

    class Config:
        orm_mode = True
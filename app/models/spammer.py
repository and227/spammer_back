from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from models.base import ActiveBase, TimestampBase

class User(ActiveBase, TimestampBase):
    __tablename__ = 'spammers'

    id = Column(Integer, primary_key=True)
    name: str
    target: HttpUrl
    state: SpammerStateEnum = SpammerStateEnum.idle
    progress: int
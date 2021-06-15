from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Enum

from schemas.spammer import SpammerStateEnum
from db.base_class import Base


class Spammer(Base):
    spammer_type = Column(String, default='vk')
    login = Column(String)
    target = Column(String)
    target_type = Column(String, default='post')
    current = Column(Integer, default=0)
    total = Column(Integer, default=0)
    state = Column(
        Enum(SpammerStateEnum),
        default=SpammerStateEnum.stopped
    )

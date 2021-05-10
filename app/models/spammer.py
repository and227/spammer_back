from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Enum
from schemas.spammer import SpammerStateEnum
from db.base_class import Base

class Spammer(Base):
    name = Column(String)
    target = Column(String)
    state = Column(
        Enum(SpammerStateEnum),
        default=SpammerStateEnum.idle
    )
    progress = Column(Integer, default=0)

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Enum

from schemas.spammer import SpammerStateEnum
from db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type


class Spammer(Base):
    script_template = Column(String)
    login = Column(String)
    password = Column(String)
    options = Column(mutable_json_type(dbtype=JSONB, nested=True))
    state = Column(
        Enum(SpammerStateEnum),
        default=SpammerStateEnum.stopped
    )
    statistics = Column(mutable_json_type(dbtype=JSONB, nested=True))
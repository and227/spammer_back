from db import Base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime

class ActiveBase(Base):
    is_active = Column(Boolean, default=False)

class TimestampBase(Base):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
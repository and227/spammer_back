from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from models.base import ActiveBase, TimestampBase

class User(ActiveBase, TimestampBase):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String, unique=True)

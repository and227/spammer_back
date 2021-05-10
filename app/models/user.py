from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from db.base_class import Base

class User(Base):    
    email = Column(String, unique=True)
    hashed_password = Column(String, unique=True)

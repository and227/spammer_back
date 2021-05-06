from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine

from core.config import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)
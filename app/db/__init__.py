from sqlalchemy.engine import create_engine

from core.config import settings

engine = create_engine(settings.DATABASE_URL)
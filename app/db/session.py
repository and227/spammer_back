from sqlalchemy.orm import sessionmaker, Session
from db import engine

DatabaseSession = sessionmaker(bind=engine)

def get_database_session() -> Session:
    db = DatabaseSession()
    try: 
        yield db
    finally:
        db.close()
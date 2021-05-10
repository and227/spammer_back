from fastapi import FastAPI
from api import api
from db.base_class import Base
from db import engine

app = FastAPI()

app.include_router(api.router)

Base.metadata.create_all(bind=engine)
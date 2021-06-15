from pydantic import BaseModel

class BaseResult(BaseModel):
    status: str

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserIn(UserBase):
    password: str

class UserStore(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True
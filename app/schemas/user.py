from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator


class UserBase(BaseModel):
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserInRegister(UserIn):
    @validator('password')
    def check_password(cls, value, values, **kwargs):
        check = True
        message = ''
        symbols = ['!', '?', '-', '_', '#', '$']

        if len(value) < 8:
            message = 'Password should be at least 8 characters'
            check = False
        elif not any(char.islower() for char in value): 
            message = 'Password should have at least one lowercase letter.'
            check = False
        elif not any(char.isupper() for char in value): 
            message = 'Password should have at least one uppercase letter.'
            check = False
        elif not any(char.isdigit() for char in value): 
            message = 'Password should have at least one number.'
            check = False
        elif not any(char in symbols for char in value): 
            message = 'Password should have at least one of the symbols: !?-_#$%*().'
            check = False               

        if check:
            return value
        else:
            raise ValueError(message)


class UserStore(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True

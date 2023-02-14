from pydantic import BaseModel
from typing import Union
from pydantic import constr,EmailStr 


class UserRequest(BaseModel):
    username:constr(min_length=1)
    password:constr(min_length=1)
    email:EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserResponse(BaseModel):
    username:str
    email:str
    id:int
    token:Token
    class Config():
        orm_mode=True

class TokenUserResponse(BaseModel):
    username:str
    email:str
    id:int
    class Config():
        orm_mode=True


    class Config():
        orm_mode=True

class LoginRequest(BaseModel):
    username:str
    password:str

    class Config():
        orm_mode=True

class LoginResponse(UserResponse):
    token:Token
    
    class Config():
        orm_mode=True

class TokenData(BaseModel):
    user_id: Union[int, None] = None
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing import Annotated
from pydantic import Field

class postModel(BaseModel):
    title:str
    content:str
    published:bool = True

class userOut(BaseModel):
    id: int
    email: EmailStr
    created_at:datetime

    class Config:
        orm_model = True


class post(BaseModel):
    id:int
    title:str
    content:str
    published:bool = True
    owner_id:int
    owner:userOut

    class Config:
            orm_model = True


class UserCreate(BaseModel):
    email: EmailStr
    password:str


class userLogin(BaseModel):
    email: EmailStr
    password: str

class token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]

class PostOut(BaseModel):
    Post: post
    votes: int
    class Config:
        orm_model = True


from pydantic import conint, BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(BasePost):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Post(BasePost):
    id: int
    created_at: datetime
    user: UserOut

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)
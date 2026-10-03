from pydantic import BaseModel , EmailStr
from typing import Optional
from  datetime import datetime
from pydantic.types import conint
from typing import Literal


class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime

    model_config = {'from_attributes': True}

class PostBase(BaseModel):
    # id: Optional[int]
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class CreatePost(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner : UserOut

    model_config = {'from_attributes' : True}

class PostOut(PostResponse):
    Post : PostResponse
    votes : int

    model_config = {'from_attributes': True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id: int
    # dir : conint(ge=0,le=1)
    dir : Literal[0 , 1]
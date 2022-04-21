
# Schemas correspond to the HTTP requests/responses


from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class Postbase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class Postcreate(Postbase):
    pass


class Post(Postbase):
    id: int
    created_at: datetime


class PostResponse(Postbase):
    id: str
    created_at: datetime
    pass


class UserCreate(BaseModel):
    # install email validator library or check if there
    email: EmailStr
    password: str

    # class Config:
    #     orm_mode = True


class User(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        # this is needed for converting orm model to pydantic response
        orm_mode = True


class UserResponse(User):
    pass

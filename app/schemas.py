
# Schemas correspond to the HTTP requests/responses


from datetime import datetime
from pydantic import BaseModel
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

from fastapi import Body, FastAPI
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str


app = FastAPI()


@app.get("/")
def root():
    return {"message": " Hello Ayman "}


@app.get("/posts")
def get_posts():
    return {"data": " this is the data requested"}


@app.post("/createposts")
def create_posts(new_post: Post):

    return {"message": "post created"}

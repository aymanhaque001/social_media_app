
from logging import raiseExceptions
from time import sleep
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2 .extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='postgres', user='postgres', password="Autopsy1", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection successful")
        break

    except Exception as error:
        print("Connecting to db failed")
        print("error:", error)
        sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index(id):
    for i, x in enumerate(my_posts):
        if x["id"] == id:
            return i


app = FastAPI()

my_posts = [{"title": "TITLE A", "content": " content of A", "id": 1},
            {"title": "TITLE B", "content": " content of B", "id": 2},
            {"title": "TITLE C", "content": " content of C", "id": 3}]


@app.get("/")
def root():
    return {"message": " Hello Ayman "}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts( title, content, published) VALUES (%s, %s , %s ) RETURNING * """,
                   (post.title, post.content, post.published))
    newpost = cursor.fetchone()
    conn.commit()
    return{"message": "Post created successfully!", "data": newpost}


@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    cursor.execute(
        """SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")
    return {f"Post {id}": post}


@ app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s returning * """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(
        """UPDATE posts SET title = %s, content = %s , published = %s  WHERE id = %s Returning * """, (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    conn.commit()
    return{"message": f"Post {id} has been updated! ", "data": post}


from datetime import datetime
from time import sleep
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2 .extras import RealDictCursor
from app.schemas import Postcreate
from .schemas import Post

from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal, get_db
from app import schemas

# The line of code below creates a table initialized in models.py for sqlalchemy if a table does not exist
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return {"message": " Hello Ayman "}


@app.get("/posts", )
def get_posts(db: Session = Depends(get_db)):

    posts = db. query(models.Post).all()

    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()

    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Postcreate, db: Session = Depends(get_db)):

    # Below code is SQL
    # # cursor.execute(""" INSERT INTO posts( title, content, published) VALUES (%s, %s , %s ) RETURNING * """,
    # #                (post.title, post.content, post.published))
    # # newpost = cursor.fetchone()
    # # conn.commit()

    # #below code is a a longer process and the uncommmented one is shortcut. With ** we unpack the dict automatically
    # newpost = models.Post(
    #     title=post.title, content=post.content, published=post.published)

    newpost = models.Post(**post.dict())

    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    print(newpost)
    return newpost


@app.get("/posts/{id}")
def get_posts(id: int, response: Response, db: Session = Depends(get_db)):
    # # Below is sql code (commented)
    # cursor.execute(
    #     """SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")
    return post


@ app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # #sql
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning * """, (str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put("/posts/{id}")
def update_post(id: int, post: Postcreate, db: Session = Depends(get_db)):

    # # SQL
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s , published = %s  WHERE id = %s Returning * """, (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # print(post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    newpost = post_query.first()
    if not newpost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


from datetime import datetime
from time import sleep
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2 .extras import RealDictCursor
from app.schemas import Postcreate
from .schemas import Post

from sqlalchemy.orm import Session
from . import models, utils
from .database import engine, SessionLocal, get_db
from app import schemas
from .routers import posts, users, auth

from . import oauth2


# The line of code below creates a table initialized in models.py for sqlalchemy if a table does not exist
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": " This is a social media backend Project "}


# models correspond to the tables in Database in contrast to schemas which points to http response models

from sqlalchemy import TEXT, TIMESTAMP, Column, Integer, String, Boolean, text
from .database import Base


class Post(Base):
    __tablename__ = 'posts'

    # define columns of the table
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # IF the table already exists in the db, changing the parameters will not commit
    # anything to the db. (Remember server_default?) so we need alembic Alembic is used to change structure of your db and migration


class User(Base):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

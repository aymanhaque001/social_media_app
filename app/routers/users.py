from .. import database, schemas, models, utils
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import Optional, List

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_users(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Performing hashing of the password using bcrypt
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    # checking if user exists with same email

    new_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if new_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

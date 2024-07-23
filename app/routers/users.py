from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/users",
    tags= ["Users"]
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    user = models.User(**new_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with user id = {id} was not found")
    return user
import models
import schemas
import utils
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model = schemas.userOut)
def create_user(user_model: schemas.UserCreate,db = Depends(get_db)):

    hashed_password = utils.hashed_password(user_model.password)

    user_data = user_model.model_dump()
    user_data["password"] = hashed_password

    new_user = models.users(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}',response_model=schemas.userOut)
def get_users(id:int,db= Depends(get_db)):
    user = db.query(models.users).filter(models.users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user data with id:{id} not found")

    return user




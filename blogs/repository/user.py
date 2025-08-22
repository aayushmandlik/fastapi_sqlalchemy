from fastapi import APIRouter,Depends,status,HTTPException
import schemas
import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from hashing import Hash


def create_user(user:schemas.User, db:Session):
    hashedpassword = Hash.bcrypt(user.password)
    # user_data = user.dict(exclude={"password"})
    # new_user = models.User(**user_data, password=hashedpassword)
    new_user = models.User(name=user.name, email=user.email, password=hashedpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(id,db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user
from fastapi import APIRouter,Depends,status,HTTPException
import schemas
import models
from database import engine,get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
models.Base.metadata.create_all(engine)
from repository import user as user_repository

router = APIRouter(prefix="/users",tags=['Users'])

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return user_repository.create_user(user,db)

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id,db: Session = Depends(get_db)):
    return user_repository.get_user_by_id(id,db)
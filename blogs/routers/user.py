from fastapi import APIRouter,Depends,status,Response,HTTPException
import schemas
import models
from database import engine,get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from routers.blog import router as blog_router
models.Base.metadata.create_all(engine)

router = APIRouter(prefix="/users",tags=['Users'])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.post("/user", response_model=schemas.UserResponse)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(user.password)
    # user_data = user.dict(exclude={"password"})
    # new_user = models.User(**user_data, password=hashedpassword)
    new_user = models.User(name=user.name, email=user.email, password=hashedpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user
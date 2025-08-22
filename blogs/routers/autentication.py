from fastapi import APIRouter,Depends,status,HTTPException
import schemas
import models
from database import get_db
from sqlalchemy.orm import Session
from hashing import Hash

router = APIRouter(prefix="/login",tags=['Authentication'])


@router.post("/")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
    return user

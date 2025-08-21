from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
import models

def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
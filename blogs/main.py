from fastapi import FastAPI,Depends,status,Response,HTTPException
import schemas
from typing import Optional
import models
from database import engine,get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from routers.blog import router as blog_router
from routers.user import router as user_router
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blog_router)
app.include_router(user_router)

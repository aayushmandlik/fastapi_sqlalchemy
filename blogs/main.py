from fastapi import FastAPI
import models
from database import engine
from routers.blog import router as blog_router
from routers.user import router as user_router
from routers.autentication import router as authentication_router
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(authentication_router)
app.include_router(blog_router)
app.include_router(user_router)
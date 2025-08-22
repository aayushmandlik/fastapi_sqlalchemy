from fastapi import FastAPI
from blogs import models
from blogs.database import engine
from blogs.routers.blog import router as blog_router
from blogs.routers.user import router as user_router
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blog_router)
app.include_router(user_router)
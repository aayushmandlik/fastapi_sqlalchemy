from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[str]


app = FastAPI()

@app.get("/")
def start():
    return {"message": "Hello"}

@app.get("/blog/{id}")
def blog_with_path_parameter(id:int):
    return {"message": f"blog with {id}"}

@app.get("/blog")
def blog_with_query_parameter(limit=10,published:bool = True,sort: Optional[str]=None):
    if published:
        return {"message": f"{limit} published blogs from db"}
    else:
        return{"message": f"{limit} unpublished blogs from db"}
    
@app.post("/blog")
def create_blog(blog: Blog):
    return {"message": f"Blog of title '{blog.title}' created"}
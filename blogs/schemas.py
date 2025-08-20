from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    # published_at: Optional[str]   

class BlogResponse(Blog):
    pass

class User(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    email: str
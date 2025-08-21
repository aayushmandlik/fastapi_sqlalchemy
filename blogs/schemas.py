from typing import Optional
from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title: str
    body: str
    # published_at: Optional[str]   

class User(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

class BlogResponse(Blog):
    creator: UserResponse
    pass
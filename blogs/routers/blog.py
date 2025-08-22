from fastapi import APIRouter,Depends,status,Response,HTTPException
import schemas
from typing import List
import models
from database import engine,get_db
from sqlalchemy.orm import Session
from repository import blog as blog_repository

models.Base.metadata.create_all(engine)

router = APIRouter(prefix="/blog",tags=['Blogs'])

@router.get("/",response_model=List[schemas.BlogResponse])
def get_all_blogs(db: Session = Depends(get_db)):
    return blog_repository.get_all(db)

@router.get("/{id}",response_model=schemas.BlogResponse)
def blog_with_id(id,response:Response,db: Session = Depends(get_db)):
    return blog_repository.get_blog_by_id(id,db)
    

# @router.get("/blog")
# def blog_with_query_parameter(limit=10,published:bool = True,sort: Optional[str]=None):
#     if published:
#         return {"message": f"{limit} published blogs from db"}
#     else:
#         return{"message": f"{limit} unpublished blogs from db"}
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog_repository.create(request,db)

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request: schemas.Blog,db: Session=Depends(get_db)):
    return blog_repository.update(id,request,db)
    

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db: Session = Depends(get_db)):
    return blog_repository.delete_blog(id,db)
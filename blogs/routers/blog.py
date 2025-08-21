from fastapi import APIRouter,Depends,status,Response,HTTPException
import schemas
from typing import List
import models
from database import engine,get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from repository import blog

models.Base.metadata.create_all(engine)

router = APIRouter(prefix="/blog",tags=['Blogs'])

@router.get("/",response_model=List[schemas.BlogResponse])
def get_all_blogs(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.get("/{id}",response_model=schemas.BlogResponse)
def blog_with_id(id,response:Response,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if not blog:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"detail":"Blog not Found"}
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not Found")
    return blog
    

# @router.get("/blog")
# def blog_with_query_parameter(limit=10,published:bool = True,sort: Optional[str]=None):
#     if published:
#         return {"message": f"{limit} published blogs from db"}
#     else:
#         return{"message": f"{limit} unpublished blogs from db"}
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # return {"message": f"Blog of title '{blog.title}' created"}

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,blog: schemas.Blog,db: Session=Depends(get_db)):
    blogid = db.query(models.Blog).filter(models.Blog.id == id)
    if not blogid.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with Id {id} not found")
    blogid.update(blog.dict())
    db.commit()
    return blog
    

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db: Session = Depends(get_db)):
    blog_delete = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} not found")
    blog_delete.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Blog with id {id} deleted"}
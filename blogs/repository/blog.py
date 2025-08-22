from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException,status
from database import get_db
import models
import schemas
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

def get_blog_by_id(id,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if not blog:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"detail":"Blog not Found"}
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not Found")
    return blog

def create(blog: schemas.Blog, db: Session):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # return {"message": f"Blog of title '{blog.title}' created"}

def update(id,blog:schemas.Blog,db:Session):
    blogid = db.query(models.Blog).filter(models.Blog.id == id)
    if not blogid.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with Id {id} not found")
    blogid.update(blog.dict())
    db.commit()
    return blog

def delete_blog(id,db: Session):
    blog_delete = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} not found")
    blog_delete.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Blog with id {id} deleted"}
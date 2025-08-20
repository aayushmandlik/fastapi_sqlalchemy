from fastapi import FastAPI,Depends,status,Response,HTTPException
import schemas
from typing import Optional
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blog")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}",response_model=schemas.BlogResponse)
def blog_with_id(id,response:Response,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if not blog:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"detail":"Blog not Found"}
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not Found")
    return blog
    

# @app.get("/blog")
# def blog_with_query_parameter(limit=10,published:bool = True,sort: Optional[str]=None):
#     if published:
#         return {"message": f"{limit} published blogs from db"}
#     else:
#         return{"message": f"{limit} unpublished blogs from db"}
    
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # return {"message": f"Blog of title '{blog.title}' created"}

@app.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,blog: schemas.Blog,db: Session=Depends(get_db)):
    blogid = db.query(models.Blog).filter(models.Blog.id == id)
    if not blogid.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with Id {id} not found")
    blogid.update(blog.dict())
    db.commit()
    return blog
    

@app.delete("/blog", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db: Session = Depends(get_db)):
    blog_delete = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} not found")
    blog_delete.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Blog with id {id} deleted"}
  

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
@app.post("/user")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(user.password)
    # user_data = user.dict(exclude={"password"})
    # new_user = models.User(**user_data, password=hashedpassword)
    new_user = models.User(name=user.name, email=user.email, password=hashedpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
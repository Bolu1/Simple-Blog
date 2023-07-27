from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(db: Session, request:schemas.ShowBlog, userInfo:schemas.TokenData):
    print(userInfo)
    new_blog = models.Blog(title=request.title, body=request.body, user_id=userInfo.username)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(db:Session, id:int):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'
    
def update(db:Session, id:int):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id}")
    blog.update(request.dict())
    db.commit()
    return 'updated'

def show(db:Session, id:int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
    return blog
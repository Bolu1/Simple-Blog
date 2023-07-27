from fastapi import APIRouter, Depends, Response, status, HTTPException
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..repository import blog
from ..helpers import oauth2

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.get("", status_code = 200, response_model=List[schemas.ShowBlog])
def all(db:Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.post('', response_model=schemas.ShowBlog)
def create(request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(db, request, current_user)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, response:Response, db:Session = Depends(get_db)):
    return blog.show(db, int)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, db: Session = Depends(get_db)):
    return blog.delete(db, id)
        
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog)
def update(id:int, request:schemas.Blog, db:Session = Depends(get_db)):
    return blog.update(db, id) 

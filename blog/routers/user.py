from fastapi import APIRouter,Depends, HTTPException
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from ..repository import user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('', response_model=schemas.ShowBlog)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    email_exists = user.find_by_email(db, request.email)
    if email_exists:
        raise HTTPException(status_code=400, detail=f"Email already in use")
    return user.create(request, db)

    
@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user(id:int, db: Session = Depends(get_db)):
    return user.show(db, id)

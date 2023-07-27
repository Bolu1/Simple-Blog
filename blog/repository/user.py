import sys
sys.path.append("..")
from ..helpers import jwt
from datetime import timedelta
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException
from ..hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm


def create(request: schemas.User, db:Session):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(db:Session, id:int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Blog with the id {id} is not available")
    return user

def find_by_email(db:Session, email:str):
    user = db.query(model.User).filter(model.User.email == email).first()
    return user

def login_user(db:Session, request:OAuth2PasswordRequestForm):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=400, detail=f"Invalid login details")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=400, detail=f"Invalid login details")
    access_token_expires = jwt.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token_expires, "token_type":"bearer"}
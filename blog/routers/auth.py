from fastapi import APIRouter, Depends
from ..repository import user
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user.login_user(db, request)
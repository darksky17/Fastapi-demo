from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal
from .. import schemas, models, utils, oauth2

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router=APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_cred:OAuth2PasswordRequestForm = Depends(),db: Session=Depends(get_db)):
  
    user= db.query(models.User).filter(models.User.email == user_cred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    access_token= oauth2.create_token({"user_id": user.id})
    return {"access_token": access_token, "token_type":"bearer"}

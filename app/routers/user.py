
from sys import prefix
from .. import models,schemas,utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Userresp)
def create_user(user:schemas.Usercreate,db: Session=Depends(get_db)):
    
    hashed_pwd= utils.hash(user.password)
    user.password= hashed_pwd
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.Userresp)
def get_user(id:int, db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
     
from wsgiref.util import request_uri
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

from  .schemas import Token_data
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes    


def create_token(data: dict):
    dummy= data.copy()

    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dummy.update({"exp":expire})

    token=jwt.encode(dummy,SECRET_KEY,algorithm=ALGORITHM)
    
    return token


def verify_token(token:str, credentials_exception):
    payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    id: int= payload.get("user_id")

    if id is None:
        raise credentials_exception
    token_data= Token_data(id=id)

    return token_data


def get_current_user(token:str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not authorize")

    return verify_token(token, credentials_exception)


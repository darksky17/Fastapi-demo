import email
import imp
from lib2to3.pytree import Base
from sqlite3 import Date
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
     title:str
     content:str
     published: bool = True

class Userresp(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime

    class Config:
        orm_mode= True

class PostCreate(PostBase):
    pass

class Postresp(PostBase):

    id:int
    created_at: datetime
    owner_id: int
    owner:Userresp

    class Config:
        orm_mode= True

class PostOut(BaseModel):
    Post:Postresp
    Votes:int



class Usercreate(BaseModel):
    email:EmailStr
    password:str




class Userlogin(BaseModel):
    email:EmailStr
    password:str 

class Token(BaseModel):
    access_token:str
    token_type:str

class Token_data(BaseModel):
    id: Optional[str]= None

class Vote(BaseModel):
    post_id:int
    dir: int
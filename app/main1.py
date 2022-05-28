
from enum import auto
import imp
from numbers import Real
from sqlite3 import Cursor
from xmlrpc.client import FastMarshaller
from app.routers.vote import vote
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


    


            







app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}






    


from click import get_current_context
from .. import models,schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.PostOut])

def lol(db: Session=Depends(get_db), current_user: int= Depends(oauth2.get_current_user), limit:int=10,skip:int=0,search:Optional[str]=""): 
    #cursor.execute("""SELECT * FROM "Posts" """)
    #posts=cursor.fetchall()
    posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results= db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results

@router.get("/{id}", response_model=schemas.PostOut)

def get_post(id: int, response: Response,db: Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM "Posts" WHERE "Id" = %s """, (str(id)))
    #post=cursor.fetchone()
    #print(post)

    post= db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    return post   


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), user_id: int= Depends(oauth2.get_current_user)):

    #cursor.execute("""DELETE FROM "Posts" WHERE "Id"= %s RETURNING *""",(str(id)))
    #post=cursor.fetchone()
    #conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    x=post.first()
    if post.first() == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  
    if x.user_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User id didnt match")
    
    post.delete(synchronize_session=False)
    db.commit()
    return{"message":"Post deleted"}
        



@router.post("/", response_model=schemas.Postresp)
def creatt(anime_list: schemas.PostCreate,db: Session=Depends(get_db), user_id : int= Depends(oauth2.get_current_user)):
    
   new__thing=models.Post(owner_id=user_id.id,**anime_list.dict())
   db.add(new__thing)
   db.commit()
   db.refresh(new__thing) 
   return  new__thing  


@router.put("/{id}", response_model=schemas.Postresp)
def update_post(id: int, anime_list:schemas.PostCreate, db: Session=Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE "Posts" SET "Title" =%s, "Content"=%s, "Published"=%s WHERE "Id" = %s RETURNING * """,(anime_list.title,anime_list.Content,anime_list.published,str(id)))
    #post=cursor.fetchone()
    #conn.commit()
    post_q= db.query(models.Post).filter(models.Post.id==id)
    post=post_q.first()

    if post== None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
   
    if post.user_id == int(current_user.id):
         post_q.update(anime_list.dict(), synchronize_session=False)
         db.commit()
         return post_q.first()
    
    else:
        print(post.user_id)
        print(current_user.id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User id didnt match")
         
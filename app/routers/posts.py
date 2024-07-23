from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oath2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix= "/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cur = conn.cursor(row_factory=dict_row)
    # posts = cur.execute("""SELECT * FROM posts""").fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post:schemas.CreatePost, db: Session = Depends(get_db), user_id:int = Depends(oath2.get_current_user)):
    # cur = conn.cursor(row_factory=dict_row)
    # post_created = cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published)).fetchone()
    # conn.commit()
    post_created = models.Post(**post.dict())
    db.add(post_created)
    db.commit()
    db.refresh(post_created)


    return post_created



@router.get("/latest", response_model= schemas.Post)
def get_latest_post(db: Session = Depends(get_db)):
    # curr = conn.cursor(row_factory=dict_row)
    # latest_post = curr.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""").fetchone()
    # conn.commit()
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return latest_post



@router.get("/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur = conn.cursor(row_factory=dict_row)
    # required_post = cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)).fetchone()
    required_post = db.query(models.Post).filter(models.Post.id == id).first()
    if required_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with id: {id} is not found")
    return required_post



@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cur = conn.cursor(row_factory=dict_row)
    # deleted_post = cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),)).fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with id = {id} was not found")
    deleted_post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model= schemas.Post)
def update_post(id:int, update_post:schemas.CreatePost, db: Session = Depends(get_db)):
    # curr = conn.cursor(row_factory=dict_row)
    # updated_post = curr.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id))).fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with id = {id} was not found")
    
    post.update(update_post.dict(), synchronize_session= False)
    db.commit()

    return post.first()
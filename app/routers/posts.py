from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oath2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix= "/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user:models.User = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cur = conn.cursor(row_factory=dict_row)
    # posts = cur.execute("""SELECT * FROM posts""").fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post:schemas.CreatePost, db: Session = Depends(get_db), user:models.User = Depends(oath2.get_current_user)):
    # cur = conn.cursor(row_factory=dict_row)
    # post_created = cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published)).fetchone()
    # conn.commit()
    post_created = models.Post(user_id= user.id, **post.dict())
    db.add(post_created)
    db.commit()
    db.refresh(post_created)


    return post_created



@router.get("/latest", response_model= schemas.Post)
def get_latest_post(db: Session = Depends(get_db), user:models.User = Depends(oath2.get_current_user)):
    # curr = conn.cursor(row_factory=dict_row)
    # latest_post = curr.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""").fetchone()
    # conn.commit()
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return latest_post



@router.get("/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user:models.User = Depends(oath2.get_current_user)):
    # cur = conn.cursor(row_factory=dict_row)
    # required_post = cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)).fetchone()
    print(user.email)
    required_post = db.query(models.Post).filter(models.Post.id == id).first()
    if required_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with id: {id} is not found")
    return required_post



@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user:models.User = Depends(oath2.get_current_user)):
    # cur = conn.cursor(row_factory=dict_row)
    # deleted_post = cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),)).fetchone()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    if deleted_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with id = {id} was not found")
    
    if deleted_post.user_id != user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "You are not authorized to delete the post")

    deleted_post_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model= schemas.Post)
def update_post(id:int, update_post:schemas.CreatePost, db: Session = Depends(get_db), user:models.User = Depends(oath2.get_current_user)):
    # curr = conn.cursor(row_factory=dict_row)
    # updated_post = curr.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id))).fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with id = {id} was not found")
    
    if post.user_id != user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "You are not authorized to update the post")
    
    post_query.update(update_post.dict(), synchronize_session= False)
    db.commit()

    return post.first()
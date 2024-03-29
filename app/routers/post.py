
from unittest import result

from sqlalchemy import func
from app import oauth2
from .. import models, schemas, utils, oauth2
import http
from typing import List, Optional
from fastapi import Body, Depends,APIRouter, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from ..database import engine, get_db
# from . import models



router = APIRouter()







@router.get("/")
async def root():
    return {"message": "Hello World"}

# , response_model = List[schemas.Post]
# , response_model = List[schemas.PostOut]
@router.get("/posts", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user), limit:int=10, skip:int=0, search: Optional[str] = ""):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    # print(limit)
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/posts", status_code =status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # print(post.information)
    # cursor.execute(""" insert into posts (title, information) values (%s, %s) returning *""", (post.title, post.information))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # new_post = {'hi'}
    return new_post

#title str, content str
# , response_model=schemas.PostOut
@router.get("/posts/{id}", response_model=schemas.PostOut)
def get_post(id, response:Response, db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where id =(%s)""", id)
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id==id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found" )
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT, )
def delete_post(id:int, db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    #deleting post
    # cursor.execute("""delete from posts where id = %s returning *""", str(id))
    # deleted_post = cursor.fetchone()
    # index = find_index_post(id)

    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    # my_posts.pop(index)
    # conn.commit()

    if post.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"this action is forbidden")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}")
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title = %s, information = %s ,published = %s where id = %s returning *""", (post.title, post.information, post.published, str(id)))
    # # index = find_index_post(id)
    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    # post_dict = post.dict()
    # post_dict['id']=id
    # my_posts[index] = post_dict
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"this action is forbidden")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

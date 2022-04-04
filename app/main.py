import http
# from typing import List, Optional
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
import psycopg2
# from psycopg2.extras import RealDictCursor
import time
# from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import Base, engine, get_db
from .routers import user,post, auth
from .config import settings
# print(settings.database_password)




models.Base.metadata.create_all(bind=engine)


app = FastAPI()
# Dependency




# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '123456', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)


my_posts = [{
        "title": "florida beach 1",
        "content": "good",
        "published": True,
        "rating": None,
        "id":1
    },
    {
        "title": "florida beach 2",
        "content": "good",
        "published": True,
        "rating": None,
        "id":2
    }
    ]


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/posts")
# def get_posts(db: Session = Depends(get_db), response_model = List[schemas.Post]):
#     # cursor.execute("""select * from posts""")
#     # posts = cursor.fetchall()
#     # print(posts)
#     posts = db.query(models.Post).all()
#     return posts


# @app.post("/posts", status_code =status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # print(post.information)
#     # cursor.execute(""" insert into posts (title, information) values (%s, %s) returning *""", (post.title, post.information))
#     # new_post = cursor.fetchone()
#     # conn.commit()
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     # new_post = {'hi'}
#     return new_post

# #title str, content str

# @app.get("/posts/{id}", response_model=schemas.Post)
# def get_post(id, response:Response, db: Session = Depends(get_db)):
#     # cursor.execute("""select * from posts where id =(%s)""", id)
#     # post = cursor.fetchone()
#     post = db.query(models.Post).filter(models.Post.id==id).first()
#     if not post:
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message':f"post with id {id} was not found"}
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found" )
#     return post

# def find_post(id:int):
#     for p in my_posts:
#         # print(type(id))        # if "id" in p:
            
#         if p["id"]==id:
#             return p

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT )
# def delete_post(id:int, db: Session = Depends(get_db)):
#     #deleting post
#     # cursor.execute("""delete from posts where id = %s returning *""", str(id))
#     # deleted_post = cursor.fetchone()
#     # index = find_index_post(id)

#     post = db.query(models.Post).filter(models.Post.id==id)
#     if post.first()==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
#     # my_posts.pop(index)
#     # conn.commit()
#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id']==id:
#             return i

# @app.put("/posts/{id}")
# def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
#     # cursor.execute("""update posts set title = %s, information = %s ,published = %s where id = %s returning *""", (post.title, post.information, post.published, str(id)))
#     # # index = find_index_post(id)
#     # updated_post = cursor.fetchone()

#     post_query = db.query(models.Post).filter(models.Post.id==id)
#     post = post_query.first()

#     if post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
#     # post_dict = post.dict()
#     # post_dict['id']=id
#     # my_posts[index] = post_dict
#     post_query.update(updated_post.dict(), synchronize_session=False)
#     db.commit()
#     return post_query.first()

# @app.post("/users", status_code =status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # print(post.information)
#     # cursor.execute(""" insert into posts (title, information) values (%s, %s) returning *""", (post.title, post.information))
#     # new_post = cursor.fetchone()
#     # conn.commit()

#     hashed_password  = utils.hash(user.password)
#     user.password=hashed_password
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     # new_post = {'hi'}
#     return new_user


# @app.get('/users/{id}',response_model=schemas.UserOut)
# def get_user(id: int,  db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with id {id} not found")
#     return user


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
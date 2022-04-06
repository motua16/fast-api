from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class PostBase(BaseModel):
    title:str
    information:str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at:datetime
    class Config:
        orm_mode=True

class Post(PostBase):
    
    created_at:datetime
    id: int
    owner_id: int
    owner: UserOut


    class Config:
        orm_mode=True





class PostUpdate(PostBase):
    pass

# class Post(BaseModel):
#     title:str
#     information:str
#     published: bool = True
#     # rating: Optional[int] = None


# class UpdatePost(BaseModel):
#     title:str
#     information:str
#     published: bool = True
#     # rating: Optional[int] = None
class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1, ge=0)

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
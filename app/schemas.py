from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: str
    password: str

class User(UserBase):
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdatePassword(BaseModel):
    email:str
    old_password: str
    new_password: str

    class Config:
        orm_mode = True

class UserDelete(BaseModel):
    email:str
    password: str

    class Config:
        orm_mode = True

class UserList(BaseModel):
    usernames: List[str]

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class FileBase(BaseModel):
    title: str
    file_path: str
    public: bool

class FileCreate(FileBase):
    pass

class File(FileBase):
    id: int
    user_id: int
    category_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

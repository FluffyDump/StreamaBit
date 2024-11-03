from pydantic import BaseModel, Field, Extra
from typing import List, Optional
from datetime import datetime
from typing import List
from .models import UserRole


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: str
    password: str
    role: Optional[UserRole] = Field(None)

    class Config:
        extra = Extra.forbid

class User(UserBase):
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdatePassword(BaseModel):
    email:str
    new_email: Optional[str] = Field(None)
    old_password: str
    new_password: Optional[str] = Field(None)

    class Config:
        orm_mode = True
        extra = Extra.forbid

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
    description: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    created_at: datetime

    class Config:
        orm_mode = True

class CategoryUpdate(BaseModel):
    new_name: Optional[str] = Field(None)
    new_description: Optional[str] = Field(None)

    class Config:
        extra = Extra.forbid

class CategorieList(BaseModel):
    name: List[str]

    class Config:
        orm_mode = True



class FileBase(BaseModel):
    title: str
    file_path: str
    public: bool

class FileCreate(BaseModel):
    title: str
    public: bool
    max_downloads: Optional[int] = None
    expiration_date: datetime
    description: Optional[str] = None 

class File(FileBase):
    id: int
    user_id: int
    category_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

class FileTitleUpdate(BaseModel):
    user_id: int
    new_title: str
    password: str

    class Config:
        orm_mode = True

class FileTitleUpdated(BaseModel):
    title: str

    class Config:
        orm_mode = True

class FileDelete(BaseModel):
    user_id: int
    password: str

class TitleList(BaseModel):
    titles: List[str]

    class Config:
        orm_mode = True
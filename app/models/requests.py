from pydantic import BaseModel, Field, Extra
from typing import List, Optional
from datetime import datetime
import app.models.database as database

class UserBase(BaseModel):
    username: str

class CategoryBase(BaseModel):
    name: str
    description: str


class UserCreate(UserBase):
    email: str
    password: str
    role: Optional[database.UserRole] = Field(None)

    class Config:
        extra = Extra.forbid

class UserUpdatePassword(BaseModel):
    email:str
    new_email: Optional[str] = Field(None)
    old_password: str
    new_password: Optional[str] = Field(None)

    class Config:
        extra = Extra.forbid

class UserDelete(BaseModel):
    email:str
    password: str

    class Config:
        extra = Extra.forbid

class UserList(BaseModel):
    usernames: List[str]

    class Config:
        extra = Extra.forbid

class CategoryCreate(CategoryBase):
    class Config:
        extra = Extra.forbid

    pass

class CategoryUpdate(BaseModel):
    new_name: Optional[str] = Field(None)
    new_description: Optional[str] = Field(None)

    class Config:
        extra = Extra.forbid

class FileCreate(BaseModel):
    title: str
    public: bool
    max_downloads: Optional[int] = None
    expiration_date: datetime
    description: Optional[str] = None 

    class Config:
        extra = Extra.forbid

class FileTitleUpdate(BaseModel):
    user_id: int
    new_title: str
    password: str

    class Config:
        extra = Extra.forbid

class FileDelete(BaseModel):
    user_id: int
    password: str

    class Config:
        extra = Extra.forbid
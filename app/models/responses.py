from pydantic import BaseModel, Extra
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str

class CategoryBase(BaseModel):
    name: str
    description: str

class FileBase(BaseModel):
    title: str
    file_path: str
    public: bool

class User(UserBase):
    created_at: datetime
    email: str

    class Config:
        orm_mode = True
        extra = Extra.forbid

class Category(CategoryBase):
    created_at: datetime

    class Config:
        orm_mode = True
        extra = Extra.forbid

class CategorieList(BaseModel):
    name: List[str]

    class Config:
        orm_mode = True
        extra = Extra.forbid

class File(FileBase):
    id: int
    user_id: int
    category_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True
        extra = Extra.forbid

class TitleList(BaseModel):
    titles: List[str]

    class Config:
        orm_mode = True
        extra = Extra.forbid

class FileTitleUpdated(BaseModel):
    title: str

    class Config:
        orm_mode = True
        extra = Extra.forbid
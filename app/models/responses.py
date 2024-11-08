from pydantic import BaseModel, Extra, Field
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = Field(None)

class SubCategory(BaseModel):
    name: str

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

class NewCategory(CategoryBase):
    created_at: datetime

    class Config:
        orm_mode = True
        extra = Extra.forbid

class SubCategories(BaseModel):
    category_name: str
    sub_categories: Optional[List[SubCategory]] = Field(None)

    class Config:
        orm_mode = True
        extra = Extra.forbid

class CategorieList(BaseModel):
    name: str
    #icon: str  #For icons

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
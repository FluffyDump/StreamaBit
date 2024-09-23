from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    file_path = Column(String, index=True)
    title = Column(String, index=True)
    public = Column(Boolean, default=False)
    max_downloads = Column(Integer, nullable=True)
    download_count = Column(Integer, default=0)
    security_status = Column(Boolean, default=False)
    views = Column(Integer, default=0)
    expiration_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)


# Define other models like Comment, FileDownload, etc. similarly

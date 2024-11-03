from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey, text, Boolean, UniqueConstraint, Enum as SAEnum
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class UserRole(Enum):
    REGISTERED_USER = "registered_user"
    ADMIN = "admin"


class ApprovalStatus(Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "user"

    #PK
    user_id = Column(BigInteger, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.REGISTERED_USER, nullable=False)

    #Relationships
    file_likes = relationship("FileLike", back_populates="user")    #Access file likes of the user
    file_dislikes = relationship("FileDislike", back_populates="user")    #Access file dislikes of the user
    public_files = relationship("PublicUpload", back_populates="user")      #Access public uploads of the user
    private_files = relationship("PrivateUpload", back_populates="user")      #Access private uploads of the user
    sessions = relationship("UserSession", back_populates="user")       #Access user sessions
    file_approvals = relationship("FileApproval", back_populates="user")    #Access admin file approvals
    comments = relationship("Comment", back_populates="user")   #Access user comments


class FileLike(Base):
    __tablename__ = "file_like"

    #PK
    like_id = Column(BigInteger, primary_key=True, nullable=False)
    liked_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)
    
    #FK
    fk_user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)
    fk_public_upload_id = Column(BigInteger, ForeignKey('public_upload.public_upload_id'), nullable=False)

    #Unique constraint to ensure a user can only like a specific upload once
    __table_args__ = (UniqueConstraint('fk_user_id', 'fk_public_upload_id', name='uq_user_upload_like'),)

    #Relationships
    user = relationship("User", back_populates="file_likes")    #Access user who liked the file
    public_upload = relationship("PublicUpload", back_populates="file_likes")   #Access public upload that was liked


class FileDislike(Base):
    __tablename__ = "file_dislike"

    #PK
    dislike_id = Column(BigInteger, primary_key=True, nullable=False)
    disliked_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)
    
    #FK
    fk_user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)
    fk_public_upload_id = Column(BigInteger, ForeignKey('public_upload.public_upload_id'), nullable=False)

    # Unique constraint to ensure a user can only dislike a specific upload once
    __table_args__ = (UniqueConstraint('fk_user_id', 'fk_public_upload_id', name='uq_user_upload_dislike'),)

    #Relationships
    user = relationship("User", back_populates="file_dislikes")    #Access user who liked the file
    public_upload = relationship("PublicUpload", back_populates="file_dislikes")   #Access public upload that was liked


class UserSession(Base):
    __tablename__ = "user_session"

    #PK
    session_id = Column(BigInteger, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)
    ip_address = Column(String(45), nullable=False)

    #FK
    fk_user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)

    #Relationships
    user = relationship("User", back_populates="sessions")     #Access user who used the session


class FileApproval(Base):
    __tablename__ = "file_approval"

    #PK
    approval_id = Column(BigInteger, primary_key=True, nullable=False)
    reason = Column(String(255), nullable=True)
    action_date = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)
    status = Column(SAEnum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False)

    #FK
    fk_public_upload_id = Column(BigInteger, ForeignKey('public_upload.public_upload_id'), nullable=False)
    fk_user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)

    #Relationships
    user = relationship("User", back_populates="file_approvals")    #Access admin file approval
    public_upload = relationship("PublicUpload", back_populates="file_approvals")   #Access public upload that was liked


class Comment(Base):
    __tablename__ = "comment"

    #PK
    comment_id = Column(BigInteger, primary_key=True, nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)

    #FK
    fk_user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)
    fk_public_upload_id = Column(BigInteger, ForeignKey('public_upload.public_upload_id'), nullable=False)

    #Relationships
    user = relationship("User", back_populates="comments")    #Access user who wrote a comment
    public_upload = relationship("PublicUpload", back_populates="comments")   #Access public upload that was commented
    

class PublicUpload(Base):
    __tablename__ = "public_upload"

    #PK
    public_upload_id = Column(BigInteger, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    file_path = Column(String(255), unique=True, nullable=False)
    max_download_count = Column(BigInteger, server_default="0", nullable=True)
    download_count = Column(BigInteger, server_default="0", nullable=True)
    expiration_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP + INTERVAL '7 days'"), nullable=False)
    virus_free = Column(Boolean, server_default=text("false"), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)
    size_in_bytes = Column(BigInteger, nullable=False)
    file_hash = Column(String(64), unique=True, nullable=False)
    views = Column(BigInteger, server_default="0", nullable=True)
    like_count = Column(BigInteger, server_default="0", nullable=True)
    dislike_count = Column(BigInteger, server_default="0", nullable=True)
    comment_count = Column(BigInteger, server_default="0", nullable=True)
    admin_approved = Column(Boolean, server_default=text("false"), nullable=False)

    #FK
    fk_user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)

    #Relationships
    user = relationship("User", back_populates="public_files")    #Access user who uploaded the file
    file_likes = relationship("FileLike", back_populates="public_upload")    #Access likes for specific public upload
    file_dislikes = relationship("FileDislike", back_populates="public_upload")    #Access likes for specific public upload
    file_approvals = relationship("FileApproval", back_populates="public_upload")   #Access file approval
    comments = relationship("Comment", back_populates="public_upload")    #Access file comment
    sub_categories_association = relationship("PublicUploadSubCategory", back_populates="public_upload")   #Access file sub-category
    downloads = relationship("FileDownload", back_populates="public_upload")    #Access file downloads


class PublicUploadSubCategory(Base):
    __tablename__ = "has"

    #FK
    column_name = Column(String, primary_key=True)
    fk_public_upload_id = Column(BigInteger, ForeignKey('public_upload.public_upload_id'), nullable=False)
    fk_sub_category_id = Column(BigInteger, ForeignKey('sub_category.sub_category_id'), nullable=False)

    # Unique constraint to ensure a specific pair is unique
    __table_args__ = (UniqueConstraint('fk_public_upload_id', 'fk_sub_category_id', name='uq_public_upload_sub_category'),)

    #Relationships
    public_upload = relationship("PublicUpload", back_populates="sub_categories_association")   #Access public upload that is placed in sub-category
    sub_category = relationship("SubCategory", back_populates="public_uploads")    #Access sub-category


class SubCategory(Base):
    __tablename__ = "sub_category"

    #PK
    sub_category_id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    #FK
    fk_category_id = Column(BigInteger, ForeignKey('category.category_id'), nullable=False)

    #Relationships
    categories = relationship("Category", back_populates="sub_categories")    #Access category
    public_uploads = relationship("PublicUploadSubCategory", back_populates="sub_category")     #Access sub-category upload


class PrivateUpload(Base):
    __tablename__ = "private_upload"

    #PK
    private_upload_id = Column(BigInteger, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    file_path = Column(String(255), unique=True, nullable=False)
    max_download_count = Column(BigInteger, server_default="0", nullable=True)
    download_count = Column(BigInteger, server_default="0", nullable=True)
    expiration_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP + INTERVAL '7 days'"), nullable=False)
    virus_free = Column(Boolean, server_default=text("false"), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)
    size_in_bytes = Column(BigInteger, nullable=False)
    file_hash = Column(String(64), unique=True, nullable=False)
    views = Column(BigInteger, server_default="0", nullable=True)
    password_protected = Column(Boolean, nullable=False)
    password_hash = Column(String(255), nullable=True)
    download_link = Column(String(2083), nullable=False)

    #FK
    fk_user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)

    #Relationships
    user = relationship("User", back_populates="private_files")    #Access user who uploaded the file
    downloads = relationship("FileDownload", back_populates="private_upload")    #Access file downloads


class FileDownload(Base):
    __tablename__ = "file_download"

    #PK
    download_id = Column(BigInteger, primary_key=True, nullable=False)
    download_date = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)
    successful = Column(Boolean, nullable=False)
    ip_address = Column(String(45), nullable=False)

    #FK
    fk_private_upload_id = Column(BigInteger, ForeignKey('private_upload.private_upload_id'), nullable=True)
    fk_public_upload_id = Column(BigInteger, ForeignKey('public_upload.public_upload_id'), nullable=True)

    #Relationships
    private_upload = relationship("PrivateUpload", back_populates="downloads")   #Access private upload that was downloaded
    public_upload = relationship("PublicUpload", back_populates="downloads")   #Access public upload that was downloaded


class Category(Base):
    __tablename__ = "category"

    #PK
    category_id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)

    #Relationships
    sub_categories = relationship("SubCategory", back_populates="categories")   #Access sub-categories
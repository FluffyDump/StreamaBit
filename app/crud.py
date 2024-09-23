from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, password_hash=user.password, role="registered_user")
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, new_password: str):
    db_existing_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not db_existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_existing_user.password_hash = new_password 

    try:
        db.commit()
        db.refresh(db_existing_user)
        return db_existing_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_user_by_username_or_email(db: Session, username: str = None, email: str = None):
    query = db.query(models.User)
    
    if username:
        query = query.filter(models.User.username == username)
    
    if email:
        query = query.filter(models.User.email == email)

    return query.first()

def get_all_user_data(db: Session, username: str, email: str, password_hash: str):
    query = db.query(models.User)
    
    query = query.filter(models.User.username == username, models.User.email == email, models.User.password_hash == password_hash)

    return query.first()

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
def get_all_users(db: Session):
    usernames = db.query(models.User.username).all()
    username_list = [username[0] for username in usernames]
    return schemas.UserList(usernames=username_list)




def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def list_categories(db: Session):
    return db.query(models.Category).all()

def create_file(db: Session, file: schemas.FileCreate, user_id: int):
    db_file = models.File(**file.dict(), user_id=user_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id).first()

def list_files(db: Session):
    return db.query(models.File).all()

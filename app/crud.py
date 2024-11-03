from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc

def create_user(db: Session, user: schemas.UserCreate):

    if user.role:
        role_value = models.UserRole[user.role]
    else:
        role_value = models.UserRole.registered_user

    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=user.password,
        role=role_value
    )
    
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
        raise HTTPException(status_code=500, detail=str(e))


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, new_password: str, new_email: str):
    db_existing_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    
    if not db_existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if new_password is not None:
        db_existing_user.password_hash = new_password 
    if new_email is not None:
        db_existing_user.email = new_email

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

def get_user_by_username_email_id(db: Session, username: str = None, email: str = None, id: int = None):
    query = db.query(models.User)
    
    if username:
        username_query = query.filter(models.User.username == username)
        user = username_query.first()
        if user:
            return user
    
    if email:
        email_query = query.filter(models.User.email == email)
        user = email_query.first()
        if user:
            return user

    if id:
        id_query = query.filter(models.User.id == id)
        user = id_query.first()
        if user:
            return user

    return None

def get_all_user_data(db: Session, username: str, email: str, password_hash: str):
    query = db.query(models.User)
    
    query = query.filter(models.User.username == username, models.User.email == email, models.User.password_hash == password_hash)

    return query.first()

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()

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




def get_category_by_name(db: Session, name: str):
    query = db.query(models.Category)
    
    query = query.filter(models.Category.name == name)

    return query.first()

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

def get_category(db: Session, category_name: str):
    return db.query(models.Category).filter(models.Category.name == category_name).first()

def update_category(db: Session, category_name: str, new_name: str = None, new_description: str = None):
    category = db.query(models.Category).filter(models.Category.name == category_name).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category.name == new_name or category.description == new_description:
        raise HTTPException(status_code=400, detail="Category new_name or new_description must be different than previously saved")

    if new_name is not None:
        category.name = new_name
    if new_description is not None:
        category.description = new_description

    try:
        db.commit()
        db.refresh(category)
        return category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
def delete_category_by_name(db: Session, category_name: str):
    category = db.query(models.Category).filter(models.Category.name == category_name).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    try:
        db.delete(category)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def get_all_categories(db: Session):
    categories = db.query(models.Category.name).all()
    categories_list = [category[0] for category in categories]
    return schemas.CategorieList(name=categories_list)

def get_files_by_category(db: Session, category_name: str):
    category = db.query(models.Category).filter(models.Category.name == category_name).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    files = db.query(models.File).filter(models.File.category_id == category.id).all()
    
    files_list = [file.title for file in files]

    if not files_list:
        raise HTTPException(status_code=404, detail="No files found in this category")

    return {"name": files_list}









def create_file(db: Session, file: schemas.FileCreate, user_id: int, file_path: str, category_id: int, security_status: bool, views: int):
    db_file = models.File(
        user_id=user_id,
        title=file.title,
        category_id=category_id,
        file_path=file_path,
        public=file.public,
        max_downloads=file.max_downloads,
        security_status=security_status,
        views=views,
        expiration_date=file.expiration_date,
        description=file.description
    )

    try:
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        return db_file
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

def update_file_title(db: Session, file_id: int, new_title: str):
    db_file = get_file(db, file_id)
    if db_file:
        db_file.title = new_title
        try:
            db.commit()
            db.refresh(db_file)
            return db_file
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="An unexpected error occurred")
    return None

def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.file_id == file_id).first()

def delete_file(db: Session, file_id: int):
    db_file = db.query(models.File).filter(models.File.file_id == file_id).first()
    if db_file:
        db.delete(db_file)
        db.commit()

def get_file_titles(db: Session):
    titles = db.query(models.File.title).all()
    titles_list = [title[0] for title in titles]
    return titles_list
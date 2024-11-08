from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
import app.models.database as models
import app.models.requests as requestModel
import app.models.responses as responseModel
from sqlalchemy import exc

    
def get_all_users(db: Session):
    usernames = db.query(models.User.username).all()
    username_list = [username[0] for username in usernames]
    return requestModel.UserList(usernames=username_list)






    
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


def get_files_by_category(db: Session, category_name: str):
    category = db.query(models.Category).filter(models.Category.name == category_name).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    files = db.query(models.File).filter(models.File.category_id == category.id).all()
    
    files_list = [file.title for file in files]

    if not files_list:
        raise HTTPException(status_code=404, detail="No files found in this category")

    return {"name": files_list}









def create_file(db: Session, file: requestModel.FileCreate, user_id: int, file_path: str, category_id: int, security_status: bool, views: int):
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
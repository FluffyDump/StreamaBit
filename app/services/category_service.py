from app.crud import shared_crud, category_crud
from app.validators import category_validator
import app.models.requests as requestModel
from app.config.logger import logger
from sqlalchemy.orm import Session
from fastapi import HTTPException


#Create new category - validate inputs, check for existing category and create a new category object with fields: category_name and description
def create_category(db: Session, category: requestModel.CategoryCreate):
    try:
        logger.info("\nCREATING CATEGORY") 
        category_validator.validate_category_name(category_name=category.name)

        if category.description:
            category_validator.validate_category_description(description=category.description)
        else:
            logger.info("CATEGORY DESCRIPTION NOT PROVIDED, PROCEEDING FURTHER")


        existing_category = category_crud.get_category_by_name(db=db, name=category.name)
        if existing_category:
            raise HTTPException(status_code=409, detail="Category already exists")

        category = category_crud.create_category(db=db, category=category)

        shared_crud.flush(db=db)
        
        ###Add check based on if user has jwt and if jwt role is admin, then create new category###

        shared_crud.commit(db=db)

        logger.info("\nCATEGORY HAS BEEN CREATED")

        return category
    except Exception as ex:
        logger.exception(f"\nCATEGORY HAS NOT BEEN CREATED, EXCEPTION OCCURED: {ex}")
        shared_crud.rollback(db=db)
        raise


#Parse all category objects
def get_categories(db: Session):
    try:
        logger.info("\PARSING ALL CATEGORIES")
        categories = category_crud.get_all_categories(db=db)

        shared_crud.flush(db=db)

        logger.info("\CATEGORIES PARSED SUCCESSFULLY")
        return categories
    except Exception as ex:
        logger.exception(f"\nCATEGORIES HAVE NOT BEEN PARSED, EXCEPTION OCCURED: {ex}")
        shared_crud.rollback(db=db)
        raise
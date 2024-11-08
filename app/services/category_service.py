from app.crud import shared_crud, category_crud, sub_category_crud
from app.validators import category_validator, shared_validator
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
        logger.info("\nPARSING ALL CATEGORIES")
        categories = category_crud.get_all_categories(db=db)

        logger.info("\nCATEGORIES PARSED SUCCESSFULLY")
        return categories
    except Exception as ex:
        logger.exception(f"\nCATEGORIES HAVE NOT BEEN PARSED, EXCEPTION OCCURED: {ex}")
        raise


#Parse category name with sub-categories
def get_category_with_subcategories(db: Session, category_name: str):
    try:
        logger.info("\nPARSING SPECIFIC CATEGORY WITH ALL SUB-CATEGORIES")
        category_validator.validate_category_name(category_name=category_name)

        db_category = category_crud.get_category_by_name(db=db, name=category_name)

        if db_category is None:
            logger.warning(f"\nCANNOT PARSE SPECIFIC CATEGORY OBJECT - CATEGORY WITH NAME: {category_name} NOT FOUND")
            raise HTTPException(status_code=404, detail="Category not found")

        sub_categories_list = sub_category_crud.get_sub_categories_by_category_id(db=db, category_id=db_category.category_id)

        logger.info("\nSUB-CATEGORIES PARSED SUCCESSFULLY")
    
        return {
            "category_name": db_category.name,
            "sub_categories": sub_categories_list
        }
    except Exception as ex:
        logger.exception(f"\nCATEGORY HAS NOT BEEN CREATED, EXCEPTION OCCURED: {ex}")
        raise


#Update category name or description
def update_category(db: Session, category_name: str, data: requestModel.CategoryUpdate):
    try:
        logger.info("\nUPDATING CATEGORY ACCOUNT DATA")

        if data.new_name is None and data.new_description is None:
            raise shared_validator.ValidationException("No new_name or new_description provided")

        if data.new_name is None and data.new_description is None:
            logger.warning("\nCANNOT UPDATE CATEGORY DATA - NO new_name OR new_description PROVIDED")
            raise shared_validator.ValidationException("No new_name or new_description provided")

        category_validator.validate_category_name(category_name)
        existing_category = category_crud.get_category_by_name(db=db, name=category_name)

        if not existing_category:
            logger.warning(f"\nCANNOT UPDATE CATEGORY DATA - CATEGORY WITH NAME: {category_name} NOT FOUND")
            raise HTTPException(status_code=404, detail="Category not found")

        if data.new_name:
            category_validator.validate_category_name(data.new_name)
            existing_new_category = category_crud.get_category_by_name(db=db, name=data.new_name)
            if existing_new_category and data.new_name != category_name:
                logger.warning("\nCANNOT UPDATE CATEGORY NAME - CATEGORY WITH PROVIDED new_name ALREADY EXISTS")
                raise shared_validator.ValidationException("Category with provided new_name aready exists")

        if data.new_description:
            category_validator.validate_category_description(data.new_description)

        ###Add check based on if user has jwt and if jwt role is admin, then change category data###

        updated_category = category_crud.update_category(db=db, category_name=category_name, new_name=data.new_name, new_description=data.new_description)

        shared_crud.commit(db)

        logger.info("\nSUCCESFULLY UPDATED CATEGORY DATA")
        
        return updated_category
    except Exception as ex:
        logger.exception(f"\nCATEGORY DATE HAS NOT BEEN CHANGED, EXCEPTION OCCURED: {ex}")
        shared_crud.rollback(db)
        raise
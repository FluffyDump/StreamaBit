from app.models import database as db_models, requests as requestModel 
from sqlalchemy.exc import IntegrityError
from app.config.logger import logger
from sqlalchemy.orm import Session
from fastapi import HTTPException


#Get category object by name
def get_category_by_name(db: Session, name: str):
    try:
        logger.info("Searching for category")

        if name:
            query = db.query(db_models.Category)
            query = query.filter(db_models.Category.name == name)

            return query.first()
        else:
            logger.warning("Category name is not provided")
            raise HTTPException(status_code=400, detail="Category name is not provided")
    except IntegrityError as ex:
        logger.exception(f"IntegrityError with category name={name}: {ex}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception with category name={name}: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    

#Create a new category object with provided fields: name and description(optional) 
def create_category(db: Session, category: requestModel.CategoryCreate):
    try:
        if category:
            logger.info("Attempting to create user session")

            db_category = db_models.Category(**category.dict())
            db.add(db_category)

            logger.info("Category prepared for creation, waiting for transaction commit")

            return db_category
        else:
            logger.error("Category cannot be created - provided category object input is None")
    except IntegrityError as ex:
        logger.exception(f"IntegrityError with category name={category.name}, description={category.description}: {ex}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception with category name={category.name}, description={category.description}: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    

#Parse all category objects
def get_all_categories(db: Session):
    try:
        logger.info("Attempting to parse all categories")

        categories = db.query(db_models.Category.name).all()
        ##categories = db.query(db_models.Category.name, db_models.Category.icon).all()     #For icons

        categories_list = [category[0] for category in categories]

        categories_list = [
            {"name": category.name}
            for category in categories
        ]

        #categories_list = [
        #    {"name": category.name, "icon": category.icon or ""}
        #    for category in categories
        #]      #For icons

        logger.info("Categories parsed")

        return categories_list
    except IntegrityError as ex:
        logger.exception(f"IntegrityError: {ex}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    

#Update category name and/or description
def update_category(db: Session, category_name: str, new_name: str, new_description: str):
    try:
        logger.info("Attempting to update category data")
        category = db.query(db_models.Category).filter(db_models.Category.name == category_name).first()
    
        if not category:
            logger.warning("Category cannot be updated - category with provided name not found")
            raise HTTPException(status_code=404, detail="Category not found")

        if new_name is not None:
            category.name = new_name
        if new_description is not None:
            category.description = new_description

        logger.info("Category prepared to get fields updated, waiting for transaction commit")

        return category
    except IntegrityError as ex:
        logger.exception(f"IntegrityError with category name={category.name}, new_name={new_name}, new_description={new_description}: {ex}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception with category name={category.name}, new_name={new_name}, new_description={new_description}: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
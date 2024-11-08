from app.models import database as db_models
from sqlalchemy.exc import IntegrityError
from app.config.logger import logger
from sqlalchemy.orm import Session
from fastapi import HTTPException


#Get all sub-category objects by category object id
def get_sub_categories_by_category_id(db: Session, category_id: int):
    try:
        logger.info("Searching for sub-categories")

        if category_id:
            query = db.query(db_models.SubCategory)
            query = query.filter(db_models.SubCategory.fk_category_id == category_id)

            sub_categories = query.all()

            sub_categories_list = [
                {"name": sub_category.name}
                for sub_category in sub_categories
            ]

            return sub_categories_list
        else:
            logger.warning("Category id is not provided")
            raise HTTPException(status_code=404, detail="Category id not found")
    except IntegrityError as ex:
        logger.exception(f"IntegrityError with category id={category_id}: {ex}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception with category id={category_id}: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
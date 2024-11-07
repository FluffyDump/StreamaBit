from app.validators import shared_validator
from app.config.logger import logger

MIN_CATEGORY_NAME_LENGTH = 4
MAX_CATEGORY_NAME_LENGTH = 50

MAX_DESCRIPTION_LENGTH = 255


#Validate category name to make sure it has no SQL queries and name length is within specified bounds
def validate_category_name(category_name: str):
    logger.info(f"Validating category name")

    if category_name is not None:
        shared_validator.validate_sql_malicious_input(category_name)

        category_name_length = len(category_name)

        if category_name_length < MIN_CATEGORY_NAME_LENGTH or category_name_length > MAX_CATEGORY_NAME_LENGTH:
            logger.warning(f"Category name length out of bounds, provided category_name: {category_name}")
            raise shared_validator.ValidationException(f"Category name must be between {MIN_CATEGORY_NAME_LENGTH} and {MAX_CATEGORY_NAME_LENGTH} characters long")
        
        logger.info("Category name validation passed")
    else:
        logger.warning("No category name provided")
        raise shared_validator.ValidationException("Missing category name")
    

#
def validate_category_description(description: str):
    logger.info(f"Validating category description")

    if description is not None:
        shared_validator.validate_sql_malicious_input(description)

        if len(description) > MAX_CATEGORY_NAME_LENGTH:
            logger.warning(f"Category description length out of bounds, provided description: {description}")
            raise shared_validator.ValidationException(f"Category description must be less than {MAX_DESCRIPTION_LENGTH} characters long")
        
    logger.info("Category description validation passed")
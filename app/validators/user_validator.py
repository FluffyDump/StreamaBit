import app.validators.shared_validator as shared_validator
import app.models.database as databaseModel
from app.config.logger import logger
import re

MIN_USERNAME_LENGTH = 4
MAX_USERNAME_LENGTH = 50

MIN_EMAIL_LENGTH = 5
MAX_EMAIL_LENGTH = 100

MIN_PASSWORD_LENGTH = 8

#Validate username to make sure it has no special symbols, SQL queries.
def validate_username(username: str):
    logger.info(f"Validating username format")

    if username is not None:
        
        shared_validator.validate_sql_malicious_input(username)

        username_length = len(username)
        if username_length < MIN_USERNAME_LENGTH or username_length > MAX_USERNAME_LENGTH:
            logger.warning(f"Username length out of bounds, provided username: {username}")
            raise shared_validator.ValidationException(f"Username must be between {MIN_USERNAME_LENGTH} and {MAX_USERNAME_LENGTH} characters long")
    
        if not shared_validator.letters_numbers_only(username):
            raise shared_validator.ValidationException("Username contains special characters")
    
        logger.info("Username validation passed")
    else:
        logger.warning("None username provided")
        raise shared_validator.ValidationException("Missing username")
    

#Validate username to make sure email format is correct and email is clear of possible SQL queries
def validate_email(email: str):
    logger.info("Validating email format")
    
    if email is not None:
        shared_validator.validate_sql_malicious_input(email)

        email_length = len(email)
        if email_length < MIN_EMAIL_LENGTH or email_length > MAX_EMAIL_LENGTH:
            logger.warning(f"Email length out of bounds, provided email: {email}")
            raise shared_validator.ValidationException(f"Email must be between {MIN_EMAIL_LENGTH} and {MAX_EMAIL_LENGTH} characters long")

        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            logger.warning(f"Provided email is invalid: {email}")
            raise shared_validator.ValidationException("Invalid email format")
        
        logger.info("Email validation passed")
    else:
        logger.warning("No email provided")
        raise shared_validator.ValidationException("Missing email")


#Validate if password is long enough and if it contains at least one uppercase letter, one number and at least 1 special symbol
def validate_password(password: str): 
    logger.info("Validating password format") 

    if password is None: 
        logger.warning("No password provided") 
        raise shared_validator.ValidationException("Missing password") 
    
    if len(password) < MIN_PASSWORD_LENGTH: 
        logger.warning("Provided password is too short") 
        raise shared_validator.ValidationException(f"Password must be at least {MIN_PASSWORD_LENGTH} characters long") 
    
    if not re.search(r'[A-Z]', password): 
        logger.warning("Password must contain at least one uppercase letter") 
        raise shared_validator.ValidationException("Password must contain at least one uppercase letter") 
    
    if not re.search(r'[0-9]', password): 
        logger.warning("Password must contain at least one number") 
        raise shared_validator.ValidationException("Password must contain at least one number") 
    
    if not re.search(r'[^a-zA-Z0-9]', password): 
        logger.warning("Password must contain at least one special character") 
        raise shared_validator.ValidationException("Password must contain at least one special character") 
    logger.info("Password validation passed") 


#Validate if user role is correct - if it is defined in database enumerator
def validate_role(role: str):
    logger.info("Validating user role") 

    if role:
        shared_validator.validate_sql_malicious_input(role)

        enum_values = [enum.value for enum in databaseModel.UserRole.__members__.values()]

        try:
            valid_role = databaseModel.UserRole(role)
        except ValueError:
            logger.warning(f"Provided role is not defined: {role}") 
            raise shared_validator.ValidationException("Incorrect user role") 
        
    else:
        logger.warning("User role is None") 
        raise shared_validator.ValidationException("Missing user role") 
    
    logger.info("User role validation passed")
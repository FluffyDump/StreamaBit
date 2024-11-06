import app.validators.shared_validator as shared_validator
import app.validators.user_validator as user_validator
import app.models.requests as requestModel
from app.config.logger import logger
from sqlalchemy.orm import Session
from fastapi import HTTPException
import app.crud.user_crud as user_crud

#Creates a new user - validate inputs, roles, jwt access token, hash the password and save freshly created user
def create_user(db: Session, user: requestModel.UserCreate):
    logger.info("\nCREATING USER ACCOUNT") 
    shared_validator.validate_sql_malicious_input(user.username, user.email, user.password)
    user_validator.validate_username(user.username)
    user_validator.validate_email(user.email)
    user_validator.validate_password(user.password)
        
    if user.role:
        logger.info(f"User provided role: {user.role.value}") 
        user_validator.validate_role(user.role.value)
    else:
        logger.info("Got empty user role, proceeding further") 

    #Check role if user.role.value == databaseModel.UserRole.admin.value:
    #Add admin validation check here in the future

    existing_user = user_crud.get_by_username_email_id(db=db, username=user.username, email=user.email)
    if existing_user:
        logger.warning("\nUSER ACCOUNT CANNOT BE CREATED AS THERE IS AN EXISTING USER WITH THE SAME USERNAME OR EMAIL") 
        raise HTTPException(status_code=409, detail="Username or email already in use")
    
    #Hash and salt password in the future

    user = user_crud.create(db=db, user=user)

    if user:
        logger.info("\nUSER ACCOUNT HAS BEEN CREATED") 
    
    return user


def get_user_account_data(db: Session, username: str):
    logger.info("\nGETTING USER ACCOUNT DATA") 
    shared_validator.validate_sql_malicious_input(username)

    db_user = user_crud.get_by_username_email_id(db=db, username=username)
    if db_user is None:
        logger.warning(f"\nCANNOT GET USER ACCOUNT DATA - USER NOT FOUND") 
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info("\nUSER ACCOUNT DATA HAS BEEN PARSED") 
    return db_user
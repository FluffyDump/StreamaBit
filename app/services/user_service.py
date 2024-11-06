from app.validators import shared_validator, user_session_validator, user_validator
from app.crud import user_crud, shared_crud, user_session_crud as session_crud
import app.models.requests as requestModel
from app.config.logger import logger
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import Request

#Creates a new user - validate inputs, roles, jwt access token, hash the password and save freshly created user
def create_user(db: Session, request: Request, user: requestModel.UserCreate):
    try:
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

        shared_crud.flush(db)

        user_session_validator.validate_ip(request.client.host)
        session_crud.create(db=db, user_id=user.user_id, user_ip=request.client.host)
        logger.info("\nUSER ACCOUNT HAS BEEN CREATED")
    
        shared_crud.commit(db)
        
        return user
    except Exception as ex:
        logger.exception(f"\nUSER ACCOUNT HAS NOT BEEN CREATED, EXCEPTION OCCURED: {ex}")
        shared_crud.rollback(db)
        raise


#Parse user account specific data - email and account creation date. Method requires user username to parse account data.
def get_user_account_data(db: Session, username: str):
    try:
        logger.info("\nGETTING USER ACCOUNT DATA") 
        shared_validator.validate_sql_malicious_input(username)

        db_user = user_crud.get_by_username_email_id(db=db, username=username)
        if db_user is None:
            logger.warning(f"\nCANNOT GET USER ACCOUNT DATA - USER: {username} HAS NOT BEEN FOUND") 
            raise HTTPException(status_code=404, detail="User not found")
    
        logger.info("\nUSER ACCOUNT DATA HAS BEEN PARSED") 
        return db_user
    except Exception as ex:
        logger.exception(f"USER: {username} DATA CANNOT BE PARSED, EXCEPTION OCCURED: {ex}")
        raise


#Update user account data - email or password by given username, current email, password, optional values: new_email and new_password (one of them is required) 
def update_user(db: Session, username: str, data: requestModel.UserUpdatePassword):
    try:
        logger.info("\nUPDATING USER ACCOUNT DATA")
        shared_validator.validate_sql_malicious_input(username, data.email, data.new_email, data.password, data.new_password)

        if data.new_email is None and data.new_password is None:
            logger.warning("CANNOT UPDATE USER ACCOUNT DATA - NO new_email OR new_password PROVIDED")
            raise shared_validator.ValidationException("No new_email or new_password provided")

        user_validator.validate_username(username)
        user_validator.validate_email(data.email)
        user_validator.validate_password(data.password)

        if data.new_email:
            user_validator.validate_email(data.new_email)
        if data.new_password:
            user_validator.validate_password(data.new_password)

        if data.password == data.new_password:
            logger.warning("CANNOT UPDATE USER ACCOUNT DATA - PROVIDED new_password IS THE SAME AS PROVIDED password")
            raise shared_validator.ValidationException("Old and new passwords must be different")
        elif data.email == data.new_email:
            logger.warning("CANNOT UPDATE USER ACCOUNT DATA - PROVIDED new_email IS THE SAME AS PROVIDED email")
            raise shared_validator.ValidationException("Old and new email addresses must be different")

        #Hash old password and send it to get_authenticated_user to check if such user with such hashed password exists
        db_user = user_crud.get_authenticated_user(db=db, username=username, email=data.email, password_hash=data.password)

        shared_crud.flush(db)

        if db_user is None:
            logger.warning("CANNOT UPDATE USER ACCOUNT DATA - USER WITH PROVIDED CREDENTIALS NOT FOUND")
            raise HTTPException(status_code=404, detail="User not found")
        
        #Add new password hashing
        user_crud.update(db=db, usr_id=db_user.user_id, new_password=data.new_password, new_email=data.new_email)

        shared_crud.commit(db)

        logger.info("SUCCESFULLY UPDATED USER ACCOUNT DATA")
        
        return db_user
    except Exception as ex:
        logger.exception(f"\nUSER ACCOUNT HAS NOT BEEN CHANGED, EXCEPTION OCCURED: {ex}")
        shared_crud.rollback(db)
        raise
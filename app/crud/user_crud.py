import app.models.requests as requestModel
from sqlalchemy.exc import IntegrityError
from app.config.logger import logger
import app.models.database as models
from sqlalchemy.orm import Session
from fastapi import HTTPException


#Parse user from database by given username or email or user id
def get_by_username_email_id(db: Session, username: str = None, email: str = None, user_id: int = None):
    try:
        query = db.query(models.User)
    
        if username:
            logger.info(f"Searching for user by username: {username}")
            username_query = query.filter(models.User.username == username)
            user = username_query.first()
            if user:
                logger.info(f"User found by username: {username}")
                return user
    
        if email:
            logger.info(f"Searching for user by email: {email}")
            email_query = query.filter(models.User.email == email)
            user = email_query.first()
            if user:
                logger.info(f"User found by email: {email}")
                return user

        if user_id:
            logger.info(f"Searching for user by id: {user_id}")
            id_query = query.filter(models.User.user_id == user_id)
            user = id_query.first()
            if user:
                logger.info(f"User found by id: {user_id}")
                return user
            
        logger.info("User not found with given parameters")
        return None
    
    except IntegrityError as ex:
        logger.exception(f"IntegrityError with username={username}, email={email}, id={id}: {ex}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception with username={username}, email={email}, id={id}: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    

#Parse user by provided username, email and password
def get_authenticated_user(db: Session, username: str, email: str, password_hash: str):
    try:
        logger.info(f"Searching for user by specified username, email and password_hash")
        query = db.query(models.User) 
        query = query.filter(models.User.username == username, models.User.email == email, models.User.password_hash == password_hash)
        if query:
            logger.info(f"User found")
        else:
            logger.warning(f"User not found, specified username: {username}")
        return query.first()
    except IntegrityError as ex:
        logger.exception(f"IntegrityError with username={username}, email={email}: {ex}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception with username={username}, email={email}: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


#Create a new user by given parameters: username, email, password and role
def create(db: Session, user: requestModel.UserCreate):
    try:
        logger.info(f"Attempting to create user")

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
        logger.info("User prepared for creation, waiting for transaction commit")
        return db_user
    except IntegrityError as ex:
        logger.exception(f"IntegrityError with username={user.username}, email={user.email}, role:{role_value}: {ex}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception with username={user.username}, email={user.email}, role:{role_value}: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    

#Update user email or password by provided user id and optional values: new_password, new_email (one of them is required)
def update(db: Session, usr_id: int, new_password: str, new_email: str):
    try:
        logger.info(f"Attempting to edit user account data")
        db_existing_user = get_by_username_email_id(db=db, user_id=usr_id)
    
        if not db_existing_user:
            logger.warning(f"User not found, provided new_email: {new_email}")
            raise HTTPException(status_code=404, detail="User not found")
    
        if new_password is not None:
            db_existing_user.password_hash = new_password 
            logger.info("User prepared for password change, waiting for transaction commit")
        if new_email is not None:
            existing_email = db.query(models.User).filter(models.User.email == new_email).first()
            if not existing_email:
                db_existing_user.email = new_email
                logger.info("User prepared for email change, waiting for transaction commit")
            else:
                logger.warning("User provided new_email already exists")
                raise HTTPException(status_code=400, detail="User with such email address already exists")

        return db_existing_user

    except IntegrityError as ex:
        logger.exception(f"IntegrityError with usr_id={usr_id}, new_email={new_email}: {ex}")
        db.rollback()
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception with usr_id={usr_id}, new_email={new_email}: {ex}")
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
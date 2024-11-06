from sqlalchemy.exc import IntegrityError
from app.config.logger import logger
import app.models.database as models
from sqlalchemy.orm import Session
from fastapi import HTTPException


#Create a new user session entry in database by provided user ip
def create(db: Session, user_id: int, user_ip: str):
    try:
        logger.info(f"Attempting to create user session")

        if user_id and user_ip:
            db_session = models.UserSession(
            ip_address=user_ip,
            fk_user_id=user_id,
            )

            db.add(db_session)
            logger.info(f"Session prepared for creation, waiting for transaction commit")
        else:
            logger.error(f"Session cannot be created - user_id or user_ip not provided")

    except IntegrityError as ex:
        logger.exception(f"IntegrityError with user_id={user_id}, user_ip={user_ip}: {ex}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred")
    except Exception as ex:
        logger.exception(f"Exception with user_id={user_id}, user_ip={user_ip}: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
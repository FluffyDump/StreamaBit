from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from . import models
import json
import re

def validate_password(password: str):
    if password is not None and len(password) < 8:
        raise ValidationException("Password must be at least 8 characters long")

def validate_username(username: str):
    invalid_chars = '!*()<>?[]{}|\\;:"\'` /'

    if len(username) < 4:
        raise ValidationException("Username must be at least 4 characters long")
    
    if any(char in invalid_chars for char in username):
        raise ValidationException("Username must not contain special symbols: " + invalid_chars)

def validate_email(email: str):
    if email is not None:
        allowed_chars = '.-_@%+'
        if '@' not in email or len(email.split('@')) != 2:
            raise ValidationException("Invalid email format")
    
        local_part, domain_part = email.split('@')
    
        if (len(local_part) < 2 or
            domain_part.startswith('.') or
            '.' not in domain_part or
            domain_part.endswith('.') or
            domain_part.count('.') < 1 or
            any(char not in allowed_chars and not char.isalnum() for char in email)):
            raise ValidationException("Invalid email format")

def check_malicious_input(*args):
    malicious_patterns = [
        r"';",
        r"--",
        r"/\*",
        r"select",
        r"drop",
        r"insert",
        r"update",
        r"delete",
    ]

    pattern = re.compile("|".join(malicious_patterns), re.IGNORECASE)
    
    for arg in args:
        if arg is not None:
            if pattern.search(arg):
                raise ValidationException("Malicious input detected")
        
def validate_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
def validate_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

class ValidationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)

    def __str__(self):
        return self.detail
    
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        if error['type'] == 'value_error.missing':
            return JSONResponse(
                status_code=422,
                content={"detail": f"Field '{error['loc'][-1]}' is required."},
            )
        elif error['type'] == 'json_invalid':
            return JSONResponse(
                status_code=400,
                content={"detail": "JSON format is invalid"},
            )
        elif error['type'] == 'type_error.enum':
            return JSONResponse(
                status_code=400,
                content={"detail": "JSON format is invalid"},
            )
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request
from app.config.logger import logger
import re

class ValidationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)

    def __str__(self):
        return self.detail


#Perform a check if provided input contains letters-only
def letters_numbers_only(input: str) -> bool:
    logger.info("Validating input")
    
    if re.search(r'[^a-zA-Z0-9]', input):
        logger.warning(f"Input contains illegal chars, input string: {input}")
        return False
    
    logger.info("Input passed validation")
    return True


#Perform a check if provided input possibly contains SQL query
def validate_sql_malicious_input(*args):
    logger.info("Validating input")
    malicious_patterns = [
        r"\bselect\b",
        r"\bdrop\b",
        r"\binsert\b",
        r"\bupdate\b",
        r"\bdelete\b",
        r"\bunion\b",
        r"\balter\b",
        r"\bcreate\b",
        r"\brename\b",
        r"\btruncate\b",
        r"\bgrant\b",
        r"\brevoke\b",
        r"\bexec\b",
        r"\bexecute\b",
        r"\bxp_\b",
        r"\bsp_\b",
        r"\binformation_schema\b",
        r"\bsysobjects\b",
        r"\bsyscolumns\b"
    ]

    pattern = re.compile("|".join(malicious_patterns), re.IGNORECASE)
    
    for arg in args:
        if arg is not None:
            if pattern.search(arg):
                logger.warning(f"Input contains possible SQL query: {arg}")
                raise ValidationException("Possible malicious input detected")
    
    logger.info("Input passed validation")
    

#Custom exception validator
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
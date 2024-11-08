from fastapi import FastAPI, Depends, HTTPException, Request
from app.config.db_connection import engine, SessionLocal
from app.services import user_service, category_service
from fastapi.exceptions import RequestValidationError
import app.validators.shared_validator as validators
import app.models.responses as responseModel
import app.models.database as databaseModel
import app.models.requests as requestModel
import app.crud.user_crud as user_crud
from app.models.database import Base
from sqlalchemy.orm import Session
import app.config.logger
from typing import List
from . import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    return await validators.validation_exception_handler(request, exc)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user", response_model=responseModel.User, status_code=201,
        summary="Create a new user", 
        description="This endpoint allows you to create a new user by providing a username, email, password and role(optional). The input is validated for malicious content, and both username and email must follow the appropriate format. If the username or email is already in use, a 409 error is returned.",
        tags=["User Management"])
def create_user(user: requestModel.UserCreate, request: Request, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, request=request, user=user)


@app.get("/user/{username}", response_model=responseModel.User,
        summary="Retrieve user information", 
        description="Fetch details of a user by their username. Results include user username, email, account creation date. If the user does not exist, a 404 error is returned.",
        tags=["User Management"])
def read_user(username: str, db: Session = Depends(get_db)):
    return user_service.get_user_account_data(db=db, username=username)


@app.patch("/user/{username}", response_model=responseModel.User, status_code=200, 
        summary="Update user password or email", 
        description="Update the password or email address of a user by providing the username, email, new_email(optional), old password, and new password(optional). The input is validated to ensure that the old and new passwords(or email addresses) are different. If the user is not found, a 404 error is returned.",
        tags=["User Management"])
def update_user_credentials(username: str, data: requestModel.UserUpdatePassword, db: Session = Depends(get_db)):
    return user_service.update_user(db=db, username=username, data=data)


@app.delete("/users/{username}", status_code=204, 
        summary="Delete a user", 
        description="Delete a user from the database using their username, email, and password. If the user does not exist, a 404 error is returned. This operation requires valid credentials.",
        tags=["User Management"])
def delete_user(username: str, db: Session = Depends(get_db), data: requestModel.UserDelete = None):
    return user_service.remove_user(db=db, username=username, data=data)




@app.post("/admin/categories/", response_model=responseModel.NewCategory, status_code=201,
        summary="Create a new category", 
        description="This endpoint allows an admin to create a new category by providing a name and an optional description. Input is validated for malicious content, and a 409 error is returned if the category already exists.",
        tags=["Category Management"])
def create_category(category: requestModel.CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db=db, category=category)


@app.get("/categories/", response_model=List[responseModel.CategorieList], status_code=200,
        summary="List all categories", 
        description="Retrieve a list of all categories in the system. Endpoint and returns the names of the categories.",
        tags=["Category Management"])
def list_categories(db: Session = Depends(get_db)):
    return category_service.get_categories(db=db)


@app.get("/categories/{category_name}", response_model=responseModel.SubCategories, status_code=200,
        summary="Retrieve all specific category sub-categories", 
        description="Fetch sub-categories of a category by its name. If the category is not found, a 404 error is returned.",
        tags=["Category Management"])
def read_category(category_name: str, db: Session = Depends(get_db)):
    return category_service.get_category_with_subcategories(db=db, category_name=category_name)


@app.patch("/admin/categories/{category_name}", response_model=responseModel.NewCategory,
        summary="Update category name or description", 
        description="Update the name or description of an existing category. The existing name of the category and the new name or new description are required. Input is validated, and the updated category details are returned.",
        tags=["Category Management"])
def update_category(category_name: str, category_update: requestModel.CategoryUpdate, db: Session = Depends(get_db)):
    return category_service.update_category(db=db, category_name=category_name, data=category_update)















@app.get("/admin/users", status_code=200,
        summary="List all users", 
        description="Retrieve a list of all registered users. This endpoint is restricted to admin access and returns a list of users in the system.",
        tags=["User Management"]) #Done list all
def list_users(db: Session = Depends(get_db)): #current_user: schemas.User = Depends(get_current_active_user)):    #Admino checkas
    #if current_user.role != "admin":  #Admino checkas
        #raise HTTPException(status_code=403, detail="Not authorized to perform this action")


        ###Add check based on if user has jwt and if jwt role is admin, then return all users###

    
    users = crud.get_all_users(db=db)
    return users



@app.delete("/admin/categories/{category_name}", status_code=204,
        summary="Delete a category", 
        description="Delete a category by its name. If the category is not found, a 404 error is returned. Only admins can perform this action.",
        tags=["Category Management"]) #Done D
def delete_category(category_name: str, db: Session = Depends(get_db)):
    validators.check_malicious_input(category_name)

    ###Add check to prevent category removal if it contains sub-categories, if not - then delete category###
    ###Add check based on if user has jwt and if jwt role is admin, then delete category###

    return crud.delete_category_by_name(db=db, category_name=category_name)


################### Change to return sub-category files instead of category files
@app.get("/categories/{category_name}/files/", status_code=200,
        summary="List files in a category", 
        description="Retrieve a list of files that belong to a specific category. The category name is required, and input is validated to ensure no malicious content.",
        tags=["Category Management"])
def list_files_in_category(category_name: str, db: Session = Depends(get_db)):
    validators.check_malicious_input(category_name)

    return crud.get_files_by_category(db=db, category_name=category_name)
#################### Change to return sub-category files instead of category files



@app.post("/files/", response_model=responseModel.File, status_code=201,
        summary="Upload a new file", 
        description="This endpoint allows users to upload a new file by providing a title. The file's path is generated and stored in the database.",
        tags=["File Management"]) #Done C
def upload_file(file: requestModel.FileCreate, user_id: int, db: Session = Depends(get_db)):
    validators.check_malicious_input(file.title)

    category_id = 13
    security_status = False
    views = 0

    validators.validate_category(db=db, category_id=category_id)
    validators.validate_user(db=db, user_id=user_id)

    file_path = rf"C:\Temp\{file.title}"

    return crud.create_file(
        db=db,
        file=file,
        user_id=user_id,
        file_path=file_path,
        category_id=category_id,
        security_status=security_status,
        views=views
    )

@app.get("/{username}/{category_name}/files")

@app.get("/files/titles", response_model=responseModel.TitleList,
        summary="List all file titles", 
        description="Retrieve a list of all file titles currently stored in the system. No user authentication is required for this endpoint.",
        tags=["File Management"])
def list_file_titles(db: Session = Depends(get_db)):
    return {"titles": crud.get_file_titles(db=db)}

@app.get("/files/{file_id}", response_model=responseModel.File,
        summary="Retrieve file details", 
        description="Fetch the details of a file by its ID. If the file is not found, a 404 error is returned.",
        tags=["File Management"]) #Done R
def read_file(file_id: int, db: Session = Depends(get_db)):

    db_file = crud.get_file(db=db, file_id=file_id)

    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    return db_file

@app.patch("/files/{file_id}", response_model=responseModel.FileTitleUpdated, status_code=200,
        summary="Update file title", 
        description="Allows the owner of a file to update its title. The user must provide the correct user ID and password for validation. If the file does not belong to the user or if the password is incorrect, appropriate error messages are returned.",
        tags=["File Management"]) #Done U
def update_file_title(file_id: int, data: requestModel.FileTitleUpdate, db: Session = Depends(get_db)):
    validators.check_malicious_input(data.new_title, data.password)

    db_user = crud.get_user_by_username_email_id(db=db, id=data.user_id)
    if db_user.password_hash != data.password:
        raise HTTPException(status_code=404, detail="User not found or password incorrect")
    
    db_file = crud.get_file(db=db, file_id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if db_file.user_id != db_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    updated_file = crud.update_file_title(db=db, file_id=file_id, new_title=data.new_title)

    return updated_file

@app.delete("/files/{file_id}", status_code=204,
        summary="Delete a file", 
        description="Delete a file by its ID. The user must provide their user ID and password for validation. If the file does not belong to the user or if the password is incorrect, an error is returned. The file is permanently removed from the database.",
        tags=["File Management"]) #Done D
def delete_file(file_id: int, data: requestModel.FileDelete, db: Session = Depends(get_db)):

    validators.check_malicious_input(data.password)

    db_user = crud.get_user_by_username_email_id(db=db, id=data.user_id)
    if db_user is None or db_user.password_hash != data.password:
        raise HTTPException(status_code=404, detail="User not found or password incorrect")
    
    db_file = crud.get_file(db=db, file_id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if db_file.user_id != db_user.id:
        raise HTTPException(status_code=403, detail="User has no access to the file")

    return crud.delete_file(db=db, file_id=file_id)
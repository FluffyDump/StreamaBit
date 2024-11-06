from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from app.config.db_connection import engine, SessionLocal
from . import crud
import app.models.database as databaseModel
import app.models.requests as requestModel
import app.models.responses as responseModel
from app.models.database import Base
from sqlalchemy.orm import Session
from typing import List
import app.config.logger
import app.services.user_service as user_services
import app.validators.shared_validator as validators
import app.crud.user_crud as user_crud

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
    return user_services.create_user(db=db, user=user)


@app.get("/user/{username}", response_model=responseModel.User,
        summary="Retrieve user information", 
        description="Fetch details of a user by their username. Results include user username, email, account creation date. If the user does not exist, a 404 error is returned.",
        tags=["User Management"])
def read_user(username: str, db: Session = Depends(get_db)):
    return user_services.get_user_account_data(db=db, username=username)






@app.patch("/user/{username}", response_model=responseModel.User, status_code=200, 
        summary="Update user password or email", 
        description="Update the password or email address of a user by providing the username, email, new_email(optional), old password, and new password(optional). The input is validated to ensure that the old and new passwords(or email addresses) are different. If the user is not found, a 404 error is returned.",
        tags=["User Management"]) #Done U
def update_user_credentials(username: str, data: requestModel.UserUpdatePassword, db: Session = Depends(get_db)):

    validators.check_malicious_input(username, data.email, data.new_email, data.old_password, data.new_password)

    if data.new_email is None and data.new_password is None:
        raise HTTPException(status_code=400, detail="No new_email or new_password provided")

    validators.validate_username(username)
    validators.validate_email(data.email)
    validators.validate_email(data.new_email)
    validators.validate_password(data.old_password)
    validators.validate_password(data.new_password)

    if data.old_password == data.new_password:
        raise HTTPException(status_code=400, detail="Old and new passwords must be different")
    elif data.email == data.new_email:
        raise HTTPException(status_code=400, detail="Old and new email addresses must be different")

    db_user = crud.get_all_user_data(db=db, username=username, email=data.email, password_hash=data.old_password)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    crud.update_user(db=db, user_id=db_user.user_id, new_password=data.new_password, new_email=data.new_email)
    return db_user

@app.delete("/users/{username}", status_code=204, 
        summary="Delete a user", 
        description="Delete a user from the database using their username, email, and password. If the user does not exist, a 404 error is returned. This operation requires valid credentials.",
        tags=["User Management"]) #Done D
def delete_user(username: str, db: Session = Depends(get_db), data: requestModel.UserDelete = None):
    validators.check_malicious_input(username, data.email, data.password)
    validators.validate_username(username)
    validators.validate_email(data.email)
    validators.validate_password(data.password)
    
    db_user = crud.get_all_user_data(db=db, username=username, email=data.email, password_hash=data.password)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # JWT admino checkas
    #db_user = crud.get_user_by_username(db=db, username=username)
    #if db_user is None:
        #raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user_id=db_user.user_id)

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




@app.post("/admin/categories/", response_model=responseModel.Category, status_code=201,
        summary="Create a new category", 
        description="This endpoint allows an admin to create a new category by providing a name and an optional description. Input is validated for malicious content, and a 409 error is returned if the category already exists.",
        tags=["Category Management"]) #Done C
def create_category(category: requestModel.CategoryCreate, db: Session = Depends(get_db)):
    validators.check_malicious_input(category.name, category.description)
    existing_category = crud.get_category_by_name(db=db, name=category.name)
    if existing_category:
        raise HTTPException(status_code=409, detail="Category already exists")
    

        ###Add check based on if user has jwt and if jwt role is admin, then create new category###



    return crud.create_category(db=db, category=category)

@app.get("/categories/{category_name}", response_model=responseModel.Category,
        summary="Retrieve category details", 
        description="Fetch details of a category by its name. If the category is not found, a 404 error is returned.",
        tags=["Category Management"]) #Done R
def read_category(category_name: str, db: Session = Depends(get_db)):
    validators.check_malicious_input(category_name)

    db_category = crud.get_category(db=db, category_name=category_name)

    
    ###Return all subcategories of specific category###


    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return db_category

@app.patch("/admin/categories/{category_name}", response_model=responseModel.Category,
        summary="Update category name or description", 
        description="Update the name or description of an existing category. The existing name of the category and the new name or new description are required. Input is validated, and the updated category details are returned.",
        tags=["Category Management"]) #Done U
def update_category(category_name: str, category_update: requestModel.CategoryUpdate, db: Session = Depends(get_db)):
    validators.check_malicious_input(category_name, category_update.new_name, category_update.new_description)

    if category_update.new_name is None and category_update.new_description is None:
        raise HTTPException(status_code=400, detail="No new_name or new_description provided")
    

    ###Add check based on if user has jwt and if jwt role is admin, then patch category name and description###

    return crud.update_category(db=db, category_name=category_name, new_name=category_update.new_name, new_description=category_update.new_description)

@app.delete("/admin/categories/{category_name}", status_code=204,
        summary="Delete a category", 
        description="Delete a category by its name. If the category is not found, a 404 error is returned. Only admins can perform this action.",
        tags=["Category Management"]) #Done D
def delete_category(category_name: str, db: Session = Depends(get_db)):
    validators.check_malicious_input(category_name)

    ###Add check to prevent category removal if it contains sub-categories, if not - then delete category###
    ###Add check based on if user has jwt and if jwt role is admin, then delete category###

    return crud.delete_category_by_name(db=db, category_name=category_name)

@app.get("/categories/", status_code=200, 
        summary="List all categories", 
        description="Retrieve a list of all categories in the system. This is a public endpoint and returns the names and descriptions of the categories.",
        tags=["Category Management"]) #Done list all
def list_categories(db: Session = Depends(get_db)):

    return crud.get_all_categories(db=db)


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
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from . import models, schemas, crud, validators
from app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List


models.Base.metadata.create_all(bind=engine)

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


@app.post("/users/", response_model=schemas.User, status_code=201)  #Done C
def create_user(user: schemas.UserCreate, request: Request, db: Session = Depends(get_db)):
    try:
        validators.check_malicious_input(user.username, user.email, user.password)

        validators.validate_username(user.username)
        validators.validate_email(user.email)
        validators.validate_password(user.password)

        existing_user = crud.get_user_by_username_or_email(db=db, username=user.username, email=user.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="Username or email already in use")
        
        return crud.create_user(db=db, user=user)
    except validators.ValidationException as validation_exception:
        raise HTTPException(status_code=400, detail=str(validation_exception))

@app.get("/users/{username}", response_model=schemas.User) #Done R
def read_user(username: str, db: Session = Depends(get_db)):
    validators.check_malicious_input(username)

    db_user = crud.get_user_by_username_or_email(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.patch("/users/{username}/password", response_model=schemas.User, status_code=200) #Done U
def update_user_password(username: str, data: schemas.UserUpdatePassword, db: Session = Depends(get_db)):

    validators.check_malicious_input(username, data.email, data.old_password, data.new_password)

    validators.validate_username(username)
    validators.validate_email(data.email)
    validators.validate_password(data.old_password)
    validators.validate_password(data.new_password)

    if data.old_password == data.new_password:
        raise HTTPException(status_code=400, detail="Old and new passwords must be different")

    db_user = crud.get_all_user_data(db=db, username=username, email=data.email, password_hash=data.old_password)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    crud.update_user(db=db, user_id=db_user.id, new_password=data.new_password)

    return db_user

@app.delete("/users/{username}", status_code=204) #Done D
def delete_user(username: str, db: Session = Depends(get_db), data: schemas.UserDelete = None):
    if data:
        validators.check_malicious_input(username, data.email, data.password)
        validators.validate_username(username)
        validators.validate_email(data.email)
        validators.validate_password(data.password)
    
        db_user = crud.get_all_user_data(db=db, username=username, email=data.email, password_hash=data.password)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        # JWT admino checkas
        #db_user = crud.get_user_by_username(db=db, username=username)
        #if db_user is None:
            #raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=400, detail="Data is missing")

    crud.delete_user(db=db, user_id=db_user.id)

@app.get("/admin/users", status_code=200)
def list_users(db: Session = Depends(get_db)): #current_user: schemas.User = Depends(get_current_active_user)):    #Admino checkas
    #if current_user.role != "admin":  #Admino checkas
        #raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    
    users = crud.get_all_users(db=db)
    return users




@app.post("admin/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

@app.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.get("/categories/", response_model=List[schemas.Category])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db=db)



@app.post("/files/", response_model=schemas.File)
def upload_file(file: schemas.FileCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_file(db=db, file=file, user_id=user_id)

@app.get("/files/{file_id}", response_model=schemas.File)
def read_file(file_id: int, db: Session = Depends(get_db)):
    db_file = crud.get_file(db=db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@app.get("/files/", response_model=List[schemas.File])
def list_files(db: Session = Depends(get_db)):
    return crud.list_files(db=db)

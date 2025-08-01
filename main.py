from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db, create_table
import models, schemas, services
from auth import get_current_user, get_password_hash, authenticate_user, create_access_token
from models import User
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserCreate, Token
from datetime import timedelta

app = FastAPI(title="Bookstore API")

create_table()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Bookstore API. Use /register and /login to get started."}

@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(400, detail="Username already exists")
    hashed_pw = get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token({"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

@app.post("/books", response_model=schemas.BookResponse, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return services.create_book(db, book)

@app.get("/books", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return services.get_all_books(db)

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = services.get_book(db, book_id)
    if not book:
        raise HTTPException(404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_book = services.update_book(db, book_id, book_update)
    if not updated_book:
        raise HTTPException(404, detail="Book not found")
    return updated_book

@app.delete("/books/{book_id}", response_model=schemas.BookResponse)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted = services.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(404, detail="Book not found")
    return deleted

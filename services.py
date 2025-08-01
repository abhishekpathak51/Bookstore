from sqlalchemy.orm import Session
from models import Book
from schemas import BookCreate, BookUpdate

def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def get_all_books(db: Session):
    return db.query(Book).all()

def update_book(db: Session, book_id: int, book_update: BookUpdate):
    book = get_book(db, book_id)
    if not book:
        return None
    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if not book:
        return None
    db.delete(book)
    db.commit()
    return book

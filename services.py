from sqlalchemy.orm import Session
from models import Book
from schemas import BookCreate, BookUpdate


# Create a new book
def create_book(db: Session, book: BookCreate):
    db_instance = Book(**book.model_dump())
    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)
    return db_instance


# Get a book by ID
def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


# Get all books
def get_all_books(db: Session):
    return db.query(Book).all()


# Update a book
def update_book(db: Session, book_id: int, book_update: BookUpdate):
    db_book = get_book(db, book_id)
    if not db_book:
        return None

    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


# Delete a book
def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if not db_book:
        return None

    db.delete(db_book)
    db.commit()
    return db_book

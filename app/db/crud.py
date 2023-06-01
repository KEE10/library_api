from sqlalchemy.orm import Session

from app.db.models import Author, Book
from app.schemas import AuthorCreate, BookCreate

from typing import List

def create_author(db: Session, author: AuthorCreate) -> Author:
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int) -> Author:
    return db.query(Author).filter(Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


def update_author(db: Session, author_id: int, author: AuthorCreate) -> Author:
    db_author = db.query(Author).filter(Author.id == author_id).first()
    for key, value in author.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> Author:
    db_author = db.query(Author).filter(Author.id == author_id).first()
    db.delete(db_author)
    db.commit()
    return db_author


def create_book(db: Session, book: BookCreate, author_id: int) -> Book:
    db_book = Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int) -> Book:
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def update_book(db: Session, book_id: int, book: BookCreate) -> Book:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Book:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    db.delete(db_book)
    db.commit()
    return db_book

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.crud import create_book, delete_book, get_book, get_books, update_book
from app.schemas import BookCreate, BookUpdate, Book
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Book])
async def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve books.
    """
    books = get_books(db, skip=skip, limit=limit)
    return books


@router.post("/", response_model=Book)
async def create_book_handler(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create new book.
    """
    db_book = create_book(db, book)
    return db_book


@router.get("/{book_id}", response_model=Book)
async def read_book_handler(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve book by ID.
    """
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book


@router.put("/{book_id}", response_model=Book)
async def update_book_handler(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    """
    Update a book.
    """
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return update_book(db, db_book=db_book, book=book)


@router.delete("/{book_id}", response_model=Book)
async def delete_book_handler(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book.
    """
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return delete_book(db, db_book=db_book)

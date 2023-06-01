from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


@router.post("/authors", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@router.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.update_author(db=db, author=db_author, author_update=author)


@router.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    crud.delete_author(db=db, author=db_author)
    return {"detail": "Author deleted"}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from typing import List
from app.settings import settings
from app.schemas import Author as AuthorSchema, Book as BookSchema
from app.db.models import Author, Book

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

register_tortoise(
    app,
    db_url=settings.DB_URL,
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.post("/authors", response_model=AuthorSchema)
async def create_author(author: AuthorSchema):
    try:
        db_author = Author(name=author.name)
        await db_author.save()
        return await AuthorSchema.from_tortoise_orm(db_author)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/authors", response_model=List[AuthorSchema])
async def get_authors():
    db_authors = await Author.all()
    return await AuthorSchema.from_queryset(db_authors)


@app.get("/authors/{author_id}", response_model=AuthorSchema)
async def get_author(author_id: int):
    db_author = await Author.get_or_none(id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return await AuthorSchema.from_tortoise_orm(db_author)


@app.put("/authors/{author_id}", response_model=AuthorSchema)
async def update_author(author_id: int, author: AuthorSchema):
    db_author = await Author.get_or_none(id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db_author.name = author.name
    await db_author.save()
    return await AuthorSchema.from_tortoise_orm(db_author)


@app.delete("/authors/{author_id}")
async def delete_author(author_id: int):
    db_author = await Author.get_or_none(id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    await db_author.delete()


@app.post("/books", response_model=BookSchema)
async def create_book(book: BookSchema):
    try:
        db_book = Book(title=book.title, author_id=book.author_id)
        await db_book.save()
        return await BookSchema.from_tortoise_orm(db_book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/books", response_model=List[BookSchema])
async def get_books():
    db_books = await Book.all().prefetch_related('author')
    return await BookSchema.from_queryset(db_books)


@app.get("/books/{book_id}", response_model=BookSchema)
async def get_book(book_id: int):
    db_book = await Book.get_or_none(id=book_id).prefetch_related('author')
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return await BookSchema.from_tortoise_orm(db_book)


@app.put("/books/{book_id}", response_model=BookSchema)
async def update_book(book_id: int, book: BookSchema):
    db_book = await Book.get_or_none(id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

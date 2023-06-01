from typing import List

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True
    
    @staticmethod
    def from_tortoise_orm(author: AuthorBase) -> AuthorBase:
        return Author(**author.__dict__)

    @staticmethod
    def from_queryset(authors: List[AuthorBase]) -> List[AuthorBase]:
        return [Author(**author.__dict__) for author in authors]


class BookBase(BaseModel):
    title: str
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
    
    @staticmethod
    def from_tortoise_orm(book: BookBase) -> BookBase:
        return BookBase(**book.__dict__)

    @staticmethod
    def from_queryset(books: List[BookBase]) -> List[BookBase]:
        return [BookBase(**book.__dict__) for book in books]


class BookWithAuthor(Book):
    author: Author


class BooksWithAuthorList(BaseModel):
    books: List[BookWithAuthor]


class LoanBase(BaseModel):
    borrower_name: str
    book_id: int


class LoanCreate(LoanBase):
    pass


class Loan(LoanBase):
    id: int

    class Config:
        orm_mode = True

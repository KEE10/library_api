from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author {self.name}>"

    @classmethod
    def get_by_id(cls, db, id):
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_name(cls, db, name):
        return db.query(cls).filter(cls.name == name).first()

    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self, db):
        db.delete(self)
        db.commit()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    published_date = Column(DateTime(timezone=True), server_default=func.now())

    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"

    @classmethod
    def get_all(cls, db):
        return db.query(cls).all()

    @classmethod
    def get_by_id(cls, db, id):
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_title(cls, db, title):
        return db.query(cls).filter(cls.title == title).first()

    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self, db):
        db.delete(self)
        db.commit()

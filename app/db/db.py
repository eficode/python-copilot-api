from sqlmodel import SQLModel, create_engine, Session, Field, Relationship
from fastapi import Depends

from typing import Generator, Annotated

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author_id: int | None = Field(default=None, foreign_key="author.id")
    author: "Author" = Relationship(back_populates="books")
    published_year: int
    isbn: str
    pages: int
    price: float

class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    books: list[Book] = Relationship(back_populates="author")

DB_URL = "sqlite:///db/bookstore.db"
engine = create_engine(DB_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

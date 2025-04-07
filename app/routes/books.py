from fastapi import APIRouter
from typing import Any
from sqlmodel import select

from db.db import SessionDep, Book

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/")
def get_books(*, session: SessionDep) -> Any:
    select_query = select(Book)
    books = session.exec(select_query).all()
    if not books:
        return {"message": "No books found"}
    return {"books": books}

@router.get("/{book_id}")
def get_book(session: SessionDep, book_id: int):
    item = session.get(Book, book_id)
    if item is None:
        return {"message": "Book not found"}
    return item

@router.post("/")
def create_book(*, session: SessionDep, book: Book) -> Any:
    session.add(book)
    session.commit()
    session.refresh(book)
    return {"message": "Book created", "book": book}

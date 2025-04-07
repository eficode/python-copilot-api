from fastapi import APIRouter
from typing import Any
from sqlmodel import select

from db.db import SessionDep, Author

router = APIRouter(prefix="/authors", tags=["authors"])

@router.get("/")
def get_authors(*, session: SessionDep) -> Any:
    select_query = select(Author)
    authors = session.exec(select_query).all()
    return {"authors": authors}

@router.get("/{author_id}")
def get_author(session: SessionDep, author_id: int) -> Any:
    item = session.get(Author, author_id)
    if item is None:
        return {"message": "Author not found"}
    return item

@router.post("/")
def create_author(*, session: SessionDep, author: Author) -> Any:
    session.add(author)
    session.commit()
    session.refresh(author)
    return {"message": "Author created", "author": author}
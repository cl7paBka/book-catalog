from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ShowBook(BaseModel):
    book_id: UUID
    title: str
    author: str
    year: int
    genre: str
    pages: int
    available: bool = True
    isbn: str | None
    description: str | None
    extra: dict | None
    created_at: datetime
    updated_at: datetime

class BookCreate(ShowBook):
    title: str
    author: str
    year: int
    genre: str
    pages: int
    isbn: str | None
    description: str

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    genre: str | None = None
    pages: int | None = None
    available: bool | None = None
    isbn: str | None = None
    description: str | None = None
    extra: dict | None = None
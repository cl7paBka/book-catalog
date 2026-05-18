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
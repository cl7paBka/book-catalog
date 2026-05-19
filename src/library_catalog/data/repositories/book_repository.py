from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.data.models.book import Book
from src.library_catalog.data.repositories.base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)

    def _apply_filters(
        self,
        query: Select,
        title: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        year: int | None = None,
        available: bool | None = None,
    ) -> Select:
        if title is not None:
            query = query.where(Book.title.ilike(f"%{title}%"))
        if author is not None:
            query = query.where(Book.author.ilike(f"%{author}%"))
        if genre is not None:
            query = query.where(Book.genre.ilike(f"%{genre}%"))
        if year is not None:
            query = query.where(Book.year == year)
        if available is not None:
            query = query.where(Book.available == available)
        return query

    async def find_by_filters(
        self,
        title: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        year: int | None = None,
        available: bool | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Book]:
        """Поиск книг с фильтрацией."""
        query = self._apply_filters(
            select(Book), title, author, genre, year, available
        )
        result = await self.session.execute(query.limit(limit).offset(offset))
        return list(result.scalars().all())

    async def find_by_isbn(self, isbn: str) -> Book | None:
        """Найти книгу по ISBN."""
        result = await self.session.execute(
            select(Book).where(Book.isbn == isbn)
        )
        return result.scalar_one_or_none()

    async def count_by_filters(
        self,
        title: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        year: int | None = None,
        available: bool | None = None,
    ) -> int:
        """Подсчитать количество книг по фильтрам."""
        query = self._apply_filters(
            select(func.count(Book.book_id)), title, author, genre, year, available
        )
        result = await self.session.execute(query)
        return result.scalar_one()
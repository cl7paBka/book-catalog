from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.core.database import get_db
from src.library_catalog.data.repositories.book_repository import BookRepository
from src.library_catalog.domain.services.book_service import BookService
from src.library_catalog.external.openlibrary.client import OpenLibraryClient
from src.library_catalog.core.config import settings


# ========== EXTERNAL CLIENTS (Singletons) ==========

@lru_cache
def get_openlibrary_client() -> OpenLibraryClient:
    """
    Получить singleton OpenLibraryClient.

    lru_cache создает клиент один раз и переиспользует.
    """
    return OpenLibraryClient(
        base_url=settings.openlibrary_base_url,
        timeout=settings.openlibrary_timeout,
    )


# ========== REPOSITORIES ==========

async def get_book_repository(
        db: Annotated[AsyncSession, Depends(get_db)]
) -> BookRepository:
    """
    Создать BookRepository для текущей сессии БД.

    Создается новый экземпляр для каждого запроса.
    """
    return BookRepository(db)


# ========== SERVICES ==========

async def get_book_service(
        book_repo: Annotated[BookRepository, Depends(get_book_repository)],
        ol_client: Annotated[OpenLibraryClient, Depends(get_openlibrary_client)],
) -> BookService:
    """
    Создать BookService с внедренными зависимостями.

    FastAPI автоматически разрешит все зависимости:
    1. get_db() создаст AsyncSession
    2. get_book_repository() создаст BookRepository с session
    3. get_openlibrary_client() вернет singleton клиент
    4. Все внедрится в BookService
    """
    return BookService(
        book_repository=book_repo,
        openlibrary_client=ol_client,
    )

BookServiceDep = Annotated[BookService, Depends(get_book_service)]
BookRepoDep = Annotated[BookRepository, Depends(get_book_repository)]
DbSessionDep = Annotated[AsyncSession, Depends(get_db)]
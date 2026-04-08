"""Database engine and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import get_settings
from app.infrastructure.exceptions import DatabaseError, IntegrityConstraintError

settings = get_settings()

_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    _engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def _translate_sqlalchemy_error(exc: SQLAlchemyError) -> DatabaseError:
    """Translate SQLAlchemy exceptions into application-specific exceptions.

    Infrastructure layer translates DB exceptions into app-level exceptions.
    This keeps services free from DB implementation details.
    
    Note: This function relies on asyncpg exception class names, which are
    stable across PostgreSQL versions. Fallback string matching is provided
    for robustness but may be sensitive to PostgreSQL error message changes.
    """
    if isinstance(exc, IntegrityError):
        constraint_type = None
        table = None
        column = None
        # Try to extract structured info from the original asyncpg exception
        if exc.orig is not None:
            orig = exc.orig
            # asyncpg exceptions have class names like UniqueViolation, ForeignKeyViolation, etc.
            class_name = orig.__class__.__name__
            if class_name == "UniqueViolation":
                constraint_type = "unique"
            elif class_name == "ForeignKeyViolation":
                constraint_type = "foreign_key"
            elif class_name == "NotNullViolation":
                constraint_type = "not_null"
            elif class_name == "CheckViolation":
                constraint_type = "check"
            # Try to get table and column from orig attributes
            # asyncpg exceptions have .table_name, .column_name, .constraint_name attributes
            if hasattr(orig, "table_name"):
                table = orig.table_name
            if hasattr(orig, "column_name"):
                column = orig.column_name
            # If we still don't have constraint_type, fall back to string matching
            if constraint_type is None:
                error_str = str(orig).lower()
                if "unique" in error_str or "duplicate" in error_str:
                    constraint_type = "unique"
                elif "foreign key" in error_str or "fk_" in error_str or "is not present" in error_str:
                    constraint_type = "foreign_key"
                elif "not_null" in error_str or ("null" in error_str and "violates" in error_str):
                    constraint_type = "not_null"
                elif "check" in error_str and "violates" in error_str:
                    constraint_type = "check"
        return IntegrityConstraintError(
            message=str(exc.orig) if exc.orig else "Integrity constraint violated",
            constraint_type=constraint_type,
            table=table,
            column=column,
        )
    return DatabaseError(message="Database operation failed")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async session for FastAPI Depends.

    Infrastructure owns session lifecycle. Application services own commit.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except SQLAlchemyError as exc:
            await session.rollback()
            # Translate to application-level exception before re-raising
            db_error = _translate_sqlalchemy_error(exc)
            raise db_error from exc
        except Exception:
            await session.rollback()
            raise


async def dispose_engine() -> None:
    """Close the engine and all pooled connections."""
    await _engine.dispose()

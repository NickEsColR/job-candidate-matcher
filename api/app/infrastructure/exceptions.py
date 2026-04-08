"""Custom database exceptions for clean error handling."""

from typing import Any


class DatabaseError(Exception):
    """Base exception for database-related errors.

    Used to distinguish database errors from other application errors.
    """

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class IntegrityConstraintError(DatabaseError):
    """Raised when a database integrity constraint is violated.

    Common causes: unique constraint, foreign key violation,
    not null constraint, check constraint.
    """

    def __init__(
        self,
        message: str,
        constraint_type: str | None = None,
        table: str | None = None,
        column: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, kwargs)
        self.constraint_type = constraint_type
        self.table = table
        self.column = column


def detect_integrity_error(exc: Exception) -> tuple[bool, str, str | None]:
    """Analyze a database exception to determine if it's an integrity violation.

    Returns:
        Tuple of (is_integrity_error, constraint_type, detail_message)
    
    Note: The fallback string matching uses PostgreSQL-specific error messages,
    which may vary across PostgreSQL versions. For robust detection, rely on
    structured error info provided by IntegrityConstraintError.
    """
    # If the exception is an IntegrityConstraintError with constraint_type already set, use it
    if isinstance(exc, IntegrityConstraintError) and exc.constraint_type:
        constraint_type = exc.constraint_type
        detail_map = {
            "unique": "A record with this value already exists",
            "foreign_key": "Referenced record does not exist",
            "not_null": "A required field is missing",
            "check": "Data validation failed",
        }
        detail = detail_map.get(constraint_type, "Integrity constraint violated")
        return True, constraint_type, detail
    
    # Fallback to string matching for backward compatibility
    error_str = str(exc).lower()

    # PostgreSQL unique violation
    if "unique" in error_str or "duplicate" in error_str:
        return True, "unique", "A record with this value already exists"

    # PostgreSQL foreign key violation - "is not present" is the typical message
    if "foreign key" in error_str or "fk_" in error_str or "is not present" in error_str:
        return True, "foreign_key", "Referenced record does not exist"

    # PostgreSQL not null violation
    if "not_null" in error_str or ("null" in error_str and "violates" in error_str):
        return True, "not_null", "A required field is missing"

    # PostgreSQL check constraint
    if "check" in error_str and "violates" in error_str:
        return True, "check", "Data validation failed"

    return False, "", ""
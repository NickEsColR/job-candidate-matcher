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
    """
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
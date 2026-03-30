"""Unit tests for database exception handling."""

import pytest

from app.infrastructure.exceptions import (
    DatabaseError,
    IntegrityConstraintError,
    detect_integrity_error,
)


class TestDatabaseError:
    def test_basic_error(self) -> None:
        err = DatabaseError("Test message")
        assert err.message == "Test message"
        assert err.details == {}

    def test_error_with_details(self) -> None:
        err = DatabaseError("Test message", {"key": "value"})
        assert err.details == {"key": "value"}


class TestIntegrityConstraintError:
    def test_basic_integrity_error(self) -> None:
        err = IntegrityConstraintError("Unique violation")
        assert err.message == "Unique violation"
        assert err.constraint_type is None

    def test_integrity_error_with_metadata(self) -> None:
        err = IntegrityConstraintError(
            "Email already exists",
            constraint_type="unique",
            table="candidates",
            column="email",
        )
        assert err.constraint_type == "unique"
        assert err.table == "candidates"
        assert err.column == "email"


class TestDetectIntegrityError:
    @pytest.mark.parametrize(
        ("error_str", "expected_type", "expected_detail"),
        [
            (
                'duplicate key value violates unique constraint "candidates_email_key"',
                "unique",
                "A record with this value already exists",
            ),
            (
                "Key (id)=(999) is not present in table",
                "foreign_key",
                "Referenced record does not exist",
            ),
            (
                "null value in column 'email' violates not-null constraint",
                "not_null",
                "A required field is missing",
            ),
            (
                'new row for relation "jobs" violates check constraint "salary_check"',
                "check",
                "Data validation failed",
            ),
            (
                "Some other database error",
                "",
                "",
            ),
        ],
    )
    def test_detect_integrity_error(
        self,
        error_str: str,
        expected_type: str,
        expected_detail: str,
    ) -> None:
        class FakeExc(Exception):
            def __str__(self) -> str:
                return error_str

        is_integrity, constraint_type, detail = detect_integrity_error(FakeExc())
        assert is_integrity == (expected_type != "")
        assert constraint_type == expected_type
        assert detail == expected_detail
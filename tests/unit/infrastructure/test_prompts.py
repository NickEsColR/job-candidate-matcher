"""Unit tests for evaluation prompts."""

import pytest

from app.infrastructure.llm.prompts import SYSTEM_PROMPT, build_user_prompt
from app.schemas.evaluation import (
    CandidateEvaluationContext,
    EvaluationAnalysisInput,
    JobEvaluationContext,
)


class TestBuildUserPrompt:
    """Tests for the build_user_prompt function."""

    def test_builds_prompt_with_full_candidate_data(self) -> None:
        """Test that prompt is correctly built with complete candidate information."""
        candidate = CandidateEvaluationContext(
            skills=["Python", "FastAPI", "PostgreSQL"],
            experience_years=5,
            education="Computer Science degree",
            resume_text="Senior developer with 5 years experience...",
        )
        job = JobEvaluationContext(
            title="Senior Backend Engineer",
            description="Looking for an experienced backend developer...",
            requirements=["Python", "FastAPI", "Database design"],
        )
        input_data = EvaluationAnalysisInput(candidate=candidate, job=job)

        result = build_user_prompt(input_data)

        # Verify key sections are present
        assert "## CANDIDATE INFORMATION" in result
        assert "## JOB POSITION" in result
        assert "Senior Backend Engineer" in result
        assert "Python, FastAPI, PostgreSQL" in result
        assert "Senior developer with 5 years experience..." in result
        assert "Database design" in result

    def test_handles_empty_skills(self) -> None:
        """Test prompt handles candidate with no skills listed."""
        candidate = CandidateEvaluationContext(
            skills=[],
            experience_years=3,
        )
        job = JobEvaluationContext(
            title="Junior Developer",
            description="Entry level position",
            requirements=[],
        )
        input_data = EvaluationAnalysisInput(candidate=candidate, job=job)

        result = build_user_prompt(input_data)

        assert "None listed" in result

    def test_handles_none_values(self) -> None:
        """Test prompt handles None values gracefully."""
        candidate = CandidateEvaluationContext(
            skills=["JavaScript"],
            experience_years=None,
            education=None,
            resume_text=None,
        )
        job = JobEvaluationContext(
            title="Frontend Developer",
            description="React position",
            requirements=["JavaScript", "React"],
        )
        input_data = EvaluationAnalysisInput(candidate=candidate, job=job)

        result = build_user_prompt(input_data)

        assert "Not specified" in result
        assert "Not specified" in result
        assert "No resume/CV available" in result

    def test_handles_empty_requirements(self) -> None:
        """Test prompt handles job with no requirements."""
        candidate = CandidateEvaluationContext(
            skills=["Go", "Kubernetes"],
            experience_years=7,
        )
        job = JobEvaluationContext(
            title="DevOps Engineer",
            description="Cloud infrastructure role",
            requirements=[],
        )
        input_data = EvaluationAnalysisInput(candidate=candidate, job=job)

        result = build_user_prompt(input_data)

        assert "None specified" in result

    def test_returns_string_type(self) -> None:
        """Test that the function returns a string."""
        candidate = CandidateEvaluationContext(skills=["Python"])
        job = JobEvaluationContext(title="Developer", description="Test", requirements=[])
        input_data = EvaluationAnalysisInput(candidate=candidate, job=job)

        result = build_user_prompt(input_data)

        assert isinstance(result, str)


class TestSystemPrompt:
    """Tests for the SYSTEM_PROMPT constant."""

    def test_system_prompt_exists(self) -> None:
        """Test that SYSTEM_PROMPT is defined."""
        assert SYSTEM_PROMPT is not None
        assert isinstance(SYSTEM_PROMPT, str)

    def test_system_prompt_contains_key_instructions(self) -> None:
        """Test that system prompt contains key evaluation instructions."""
        # Check for key elements mentioned in requirements
        assert "HR analyst" in SYSTEM_PROMPT.lower() or "expert" in SYSTEM_PROMPT.lower()
        assert "score" in SYSTEM_PROMPT.lower()
        assert "0" in SYSTEM_PROMPT and "100" in SYSTEM_PROMPT
        assert "strengths" in SYSTEM_PROMPT.lower()
        assert "weaknesses" in SYSTEM_PROMPT.lower()
        assert "recommendations" in SYSTEM_PROMPT.lower()

    def test_system_prompt_is_in_english(self) -> None:
        """Test that system prompt is in English."""
        # Key phrases should be in English
        assert "You are" in SYSTEM_PROMPT
        assert "Your response must be" in SYSTEM_PROMPT

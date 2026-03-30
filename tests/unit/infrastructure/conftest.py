"""Test fixtures for infrastructure tests."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.evaluation import (
    CandidateEvaluationContext,
    EvaluationAnalysis,
    EvaluationAnalysisInput,
    JobEvaluationContext,
)


@pytest.fixture
def sample_evaluation_input() -> EvaluationAnalysisInput:
    """Provide a sample evaluation input for tests."""
    return EvaluationAnalysisInput(
        candidate=CandidateEvaluationContext(
            skills=["Python", "FastAPI", "PostgreSQL"],
            experience_years=5,
            education="Computer Science",
            resume_text="Experienced backend developer...",
        ),
        job=JobEvaluationContext(
            title="Senior Backend Engineer",
            description="Looking for experienced developer",
            requirements=["Python", "FastAPI", "Database"],
        ),
    )


@pytest.fixture
def sample_llm_response() -> EvaluationAnalysis:
    """Provide a sample LLM response for tests."""
    return EvaluationAnalysis(
        score=85,
        summary="Strong candidate with relevant experience",
        strengths=["Strong Python skills", "FastAPI experience", "5 years experience"],
        weaknesses=["No Kubernetes experience"],
        recommendations=["Learn Kubernetes", "Consider cloud certifications"],
    )


@pytest.fixture
def mock_settings():
    """Provide mock settings for testing."""
    with patch("app.infrastructure.llm.evaluation_analyzer.get_settings") as mock:
        settings = MagicMock()
        settings.llm_temperature = 0.0
        settings.llm_max_tokens = 2048
        settings.llm_base_url = None
        settings.llm_model = "gpt-4"
        settings.llm_provider = "openai"
        settings.llm_api_key = "test-key"
        settings.llm_timeout = 60
        settings.llm_max_retries = 3
        settings.llm_max_concurrency = 10
        mock.return_value = settings
        yield settings


@pytest.fixture
def mock_chat_model():
    """Provide a mock chat model for testing."""
    with patch("app.infrastructure.llm.evaluation_analyzer.init_chat_model") as mock:
        model = MagicMock()
        mock.return_value = model
        yield model


@pytest.fixture
def mock_structured_model(sample_llm_response):
    """Provide a mock structured model that returns a sample response."""
    with patch(
        "app.infrastructure.llm.evaluation_analyzer.BaseChatModel"
    ) as mock_base:
        mock_model = AsyncMock()
        mock_model.with_structured_output.return_value = AsyncMock(
            ainvoke=AsyncMock(return_value=sample_llm_response)
        )
        mock_base.return_value = mock_model
        yield mock_model

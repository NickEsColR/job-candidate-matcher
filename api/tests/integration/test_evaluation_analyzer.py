"""Real integration test for evaluation analyzer against an actual LLM provider.

This test is intentionally environment-gated and should run only when
credentials/network are available.
"""

import pytest
from pydantic import ValidationError

from app.core.settings import get_integration_test_settings, get_settings
from app.infrastructure.llm.evaluation_analyzer import LangChainEvaluationAnalyzer
from app.schemas.evaluation import (
    CandidateEvaluationContext,
    EvaluationAnalysis,
    EvaluationAnalysisInput,
    JobEvaluationContext,
)


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.integration,
]


class TestLLMOutputFormatIntegration:
    """Single end-to-end integration test using a real LLM call."""

    async def test_llm_returns_expected_structured_output(self) -> None:
        """Validate real provider call returns coherent EvaluationAnalysis output.

        Why environment-gated:
        - Avoid flaky failures in local/CI without credentials.
        - Keep unit suite deterministic.
        """
        get_integration_test_settings.cache_clear()
        integration_settings = get_integration_test_settings()

        if not integration_settings.run_llm_integration:
            pytest.skip("Set RUN_LLM_INTEGRATION=1 to execute real LLM integration test")

        # Ensure settings are loaded from real env/.env and fail fast with clear signal.
        get_settings.cache_clear()
        try:
            _ = get_settings()
        except ValidationError as exc:
            pytest.skip(f"Missing LLM settings for integration test: {exc}")

        analyzer = LangChainEvaluationAnalyzer()

        input_data = EvaluationAnalysisInput(
            candidate=CandidateEvaluationContext(
                skills=["Python", "FastAPI", "PostgreSQL"],
                experience_years=4,
                education="BSc Computer Science",
                resume_text=(
                    "Backend engineer with experience building REST APIs in Python and FastAPI, "
                    "designing relational schemas in PostgreSQL, and maintaining production services."
                ),
            ),
            job=JobEvaluationContext(
                title="Backend Engineer",
                description="Build and maintain backend services for a SaaS product.",
                requirements=["Python", "FastAPI", "PostgreSQL", "Testing"],
            ),
        )

        result = await analyzer.analyze(input_data)

        # Structured schema
        assert isinstance(result, EvaluationAnalysis)
        assert isinstance(result.score, int)
        assert 0 <= result.score <= 100
        assert isinstance(result.summary, str)
        assert len(result.summary.strip()) >= 20
        assert isinstance(result.strengths, list)
        assert isinstance(result.weaknesses, list)
        assert isinstance(result.recommendations, list)
        assert all(isinstance(item, str) for item in result.strengths)
        assert all(isinstance(item, str) for item in result.weaknesses)
        assert all(isinstance(item, str) for item in result.recommendations)

        # Coherence signal (non-empty actionable output)
        assert len(result.strengths) >= 1
        assert len(result.recommendations) >= 1

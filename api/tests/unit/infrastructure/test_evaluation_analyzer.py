"""Unit tests for LangChainEvaluationAnalyzer."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.infrastructure.llm.evaluation_analyzer import LangChainEvaluationAnalyzer
from app.schemas.evaluation import (
    CandidateEvaluationContext,
    EvaluationAnalysis,
    EvaluationAnalysisInput,
    JobEvaluationContext,
)


class TestLangChainEvaluationAnalyzerInit:
    """Tests for the analyzer initialization."""

    @patch("app.infrastructure.llm.evaluation_analyzer.get_settings")
    @patch("app.infrastructure.llm.evaluation_analyzer.init_chat_model")
    def test_initializes_with_settings(
        self, mock_init_chat_model: MagicMock, mock_get_settings: MagicMock
    ) -> None:
        """Test that analyzer initializes correctly with settings."""
        # Setup mock settings
        settings = MagicMock()
        settings.llm_temperature = 0.5
        settings.llm_max_tokens = 1024
        settings.llm_base_url = None
        settings.llm_model = "gpt-4"
        settings.llm_provider = "openai"
        settings.llm_api_key = "test-key"
        settings.llm_timeout = 30
        settings.llm_max_retries = 2
        settings.llm_max_concurrency = 5
        mock_get_settings.return_value = settings

        # Setup mock model
        mock_model = MagicMock()
        mock_init_chat_model.return_value = mock_model

        # Create analyzer
        analyzer = LangChainEvaluationAnalyzer()

        # Verify model was initialized with correct parameters
        mock_init_chat_model.assert_called_once()
        call_kwargs = mock_init_chat_model.call_args[1]
        assert call_kwargs["model"] == "gpt-4"
        assert call_kwargs["model_provider"] == "openai"
        assert call_kwargs["api_key"] == "test-key"
        assert call_kwargs["timeout"] == 30
        assert call_kwargs["max_retries"] == 2
        assert call_kwargs["temperature"] == 0.5
        assert call_kwargs["max_tokens"] == 1024

    @patch("app.infrastructure.llm.evaluation_analyzer.get_settings")
    @patch("app.infrastructure.llm.evaluation_analyzer.init_chat_model")
    def test_includes_base_url_when_provided(
        self, mock_init_chat_model: MagicMock, mock_get_settings: MagicMock
    ) -> None:
        """Test that base_url is included when provided in settings."""
        settings = MagicMock()
        settings.llm_temperature = 0.0
        settings.llm_max_tokens = 2048
        settings.llm_base_url = "https://custom.openai.com/v1"
        settings.llm_model = "gpt-4"
        settings.llm_provider = "openai"
        settings.llm_api_key = "test-key"
        settings.llm_timeout = 60
        settings.llm_max_retries = 3
        settings.llm_max_concurrency = 10
        mock_get_settings.return_value = settings

        mock_model = MagicMock()
        mock_init_chat_model.return_value = mock_model

        analyzer = LangChainEvaluationAnalyzer()

        call_kwargs = mock_init_chat_model.call_args[1]
        assert call_kwargs["base_url"] == "https://custom.openai.com/v1"

    @patch("app.infrastructure.llm.evaluation_analyzer.get_settings")
    @patch("app.infrastructure.llm.evaluation_analyzer.init_chat_model")
    def test_configures_structured_output(
        self, mock_init_chat_model: MagicMock, mock_get_settings: MagicMock
    ) -> None:
        """Test that structured output is configured."""
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
        mock_get_settings.return_value = settings

        mock_model = MagicMock()
        mock_structured = MagicMock()
        mock_model.with_structured_output.return_value = mock_structured
        mock_init_chat_model.return_value = mock_model

        analyzer = LangChainEvaluationAnalyzer()

        mock_model.with_structured_output.assert_called_once()


class TestLangChainEvaluationAnalyzerAnalyze:
    """Tests for the analyze method."""

    @pytest.mark.asyncio
    @patch("app.infrastructure.llm.evaluation_analyzer.get_settings")
    @patch("app.infrastructure.llm.evaluation_analyzer.init_chat_model")
    async def test_analyze_returns_evaluation_analysis(
        self, mock_init_chat_model: MagicMock, mock_get_settings: MagicMock
    ) -> None:
        """Test that analyze returns EvaluationAnalysis object."""
        # Setup
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
        mock_get_settings.return_value = settings

        expected_response = EvaluationAnalysis(
            score=85,
            summary="Great candidate",
            strengths=["Python", "FastAPI"],
            weaknesses=["No cloud"],
            recommendations=["Learn AWS"],
        )

        mock_model = MagicMock()
        mock_structured = AsyncMock()
        mock_structured.ainvoke = AsyncMock(return_value=expected_response)
        mock_model.with_structured_output.return_value = mock_structured
        mock_init_chat_model.return_value = mock_model

        analyzer = LangChainEvaluationAnalyzer()

        # Execute
        input_data = EvaluationAnalysisInput(
            candidate=CandidateEvaluationContext(skills=["Python", "FastAPI"]),
            job=JobEvaluationContext(
                title="Backend Dev", description="Test", requirements=["Python"]
            ),
        )
        result = await analyzer.analyze(input_data)

        # Verify
        assert isinstance(result, EvaluationAnalysis)
        assert result.score == 85
        assert result.summary == "Great candidate"

    @pytest.mark.asyncio
    @patch("app.infrastructure.llm.evaluation_analyzer.get_settings")
    @patch("app.infrastructure.llm.evaluation_analyzer.init_chat_model")
    async def test_analyze_uses_semaphore_for_concurrency(
        self, mock_init_chat_model: MagicMock, mock_get_settings: MagicMock
    ) -> None:
        """Test that analyze uses semaphore for concurrency control."""
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
        mock_get_settings.return_value = settings

        mock_model = MagicMock()
        mock_structured = AsyncMock()
        mock_structured.ainvoke = AsyncMock(
            return_value=EvaluationAnalysis(
                score=75,
                summary="Test",
                strengths=[],
                weaknesses=[],
                recommendations=[],
            )
        )
        mock_model.with_structured_output.return_value = mock_structured
        mock_init_chat_model.return_value = mock_model

        analyzer = LangChainEvaluationAnalyzer()

        # Verify semaphore was created
        assert analyzer._semaphore is not None

    @pytest.mark.asyncio
    @patch("app.infrastructure.llm.evaluation_analyzer.get_settings")
    @patch("app.infrastructure.llm.evaluation_analyzer.init_chat_model")
    async def test_analyze_includes_system_and_user_prompts(
        self, mock_init_chat_model: MagicMock, mock_get_settings: MagicMock
    ) -> None:
        """Test that analyze sends both system and user prompts."""
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
        mock_get_settings.return_value = settings

        mock_model = MagicMock()
        mock_structured = AsyncMock()
        mock_structured.ainvoke = AsyncMock(
            return_value=EvaluationAnalysis(
                score=75,
                summary="Test",
                strengths=[],
                weaknesses=[],
                recommendations=[],
            )
        )
        mock_model.with_structured_output.return_value = mock_structured
        mock_init_chat_model.return_value = mock_model

        analyzer = LangChainEvaluationAnalyzer()

        input_data = EvaluationAnalysisInput(
            candidate=CandidateEvaluationContext(skills=["Python"]),
            job=JobEvaluationContext(title="Dev", description="Test", requirements=[]),
        )
        await analyzer.analyze(input_data)

        # Verify ainvoke was called
        mock_structured.ainvoke.assert_called_once()

        # Check that the call includes system and user messages
        call_args = mock_structured.ainvoke.call_args[0][0]
        assert len(call_args) == 2
        assert call_args[0]["role"] == "system"
        assert call_args[1]["role"] == "user"
        assert "content" in call_args[0]
        assert "content" in call_args[1]

    @pytest.mark.asyncio
    @patch("app.infrastructure.llm.evaluation_analyzer.get_settings")
    @patch("app.infrastructure.llm.evaluation_analyzer.init_chat_model")
    async def test_analyze_score_bounds(
        self, mock_init_chat_model: MagicMock, mock_get_settings: MagicMock
    ) -> None:
        """Test that analyze correctly handles score values."""
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
        mock_get_settings.return_value = settings

        # Test with max score
        mock_model = MagicMock()
        mock_structured = AsyncMock()
        mock_structured.ainvoke = AsyncMock(
            return_value=EvaluationAnalysis(
                score=100,
                summary="Perfect match",
                strengths=["Perfect skills"],
                weaknesses=[],
                recommendations=[],
            )
        )
        mock_model.with_structured_output.return_value = mock_structured
        mock_init_chat_model.return_value = mock_model

        analyzer = LangChainEvaluationAnalyzer()

        input_data = EvaluationAnalysisInput(
            candidate=CandidateEvaluationContext(skills=["Python"]),
            job=JobEvaluationContext(title="Dev", description="Test", requirements=[]),
        )
        result = await analyzer.analyze(input_data)

        assert result.score == 100


class TestEvaluationAnalyzerProtocol:
    """Tests for the EvaluationAnalyzerProtocol interface."""

    def test_protocol_defines_analyze_method(self) -> None:
        """Test that the protocol defines the analyze method signature."""
        # Verify the protocol exists and has the analyze method
        from app.services.evaluation_analyzer import EvaluationAnalyzerProtocol

        assert hasattr(EvaluationAnalyzerProtocol, "analyze")

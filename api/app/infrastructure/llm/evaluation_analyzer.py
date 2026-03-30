"""LangChain-based evaluation analyzer implementation."""

import asyncio
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from app.core.settings import get_settings
from app.infrastructure.llm.prompts import SYSTEM_PROMPT, build_user_prompt
from app.schemas.evaluation import EvaluationAnalysis, EvaluationAnalysisInput
from app.services.evaluation_analyzer import EvaluationAnalyzerProtocol


class LangChainEvaluationAnalyzer(EvaluationAnalyzerProtocol):
    """LLM-based evaluation analyzer using LangChain with structured output."""

    def __init__(self) -> None:
        """Initialize the analyzer with LLM configuration from settings."""
        settings = get_settings()

        # Build model kwargs from settings
        model_kwargs: dict[str, Any] = {
            "temperature": settings.llm_temperature,
            "max_tokens": settings.llm_max_tokens,
        }

        # Add optional configuration
        if settings.llm_base_url:
            model_kwargs["base_url"] = settings.llm_base_url

        # Initialize the chat model using langchain's factory
        self._model: BaseChatModel = init_chat_model(
            model=settings.llm_model,
            model_provider=settings.llm_provider,
            api_key=settings.llm_api_key,
            timeout=settings.llm_timeout,
            max_retries=settings.llm_max_retries,
            **model_kwargs,
        )

        # Configure structured output
        # Type ignore: LangChain's with_structured_output returns a generic type that cannot
        # be precisely typed at static analysis time. The runtime behavior is correct.
        self._structured_model = self._model.with_structured_output(EvaluationAnalysis)  # type: ignore[assignment]

        # Concurrency limiter
        self._semaphore = asyncio.Semaphore(settings.llm_max_concurrency)

    async def analyze(self, input_data: EvaluationAnalysisInput) -> EvaluationAnalysis:
        """
        Analyze candidate-job match using LLM with structured output.

        Args:
            input_data: Context containing candidate and job information.

        Returns:
            EvaluationAnalysis with score, summary, strengths, weaknesses, and recommendations.
        """
        async with self._semaphore:
            user_prompt = build_user_prompt(input_data)

            # Invoke the model with structured output
            response = await self._structured_model.ainvoke(
                [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
            )

            return response  # pyright: ignore[reportReturnType]

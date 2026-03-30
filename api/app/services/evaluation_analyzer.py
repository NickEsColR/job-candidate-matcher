"""Protocol definition for evaluation analyzer."""

from typing import Protocol

from app.schemas.evaluation import EvaluationAnalysis, EvaluationAnalysisInput


class EvaluationAnalyzerProtocol(Protocol):
    """Protocol for evaluation analyzers that perform LLM-based analysis."""

    async def analyze(self, input_data: EvaluationAnalysisInput) -> EvaluationAnalysis:
        """
        Analyze candidate-job match using LLM.

        Args:
            input_data: Context containing candidate and job information.

        Returns:
            EvaluationAnalysis with score, summary, strengths, weaknesses, and recommendations.
        """
        ...

"""Background evaluation processor orchestration."""

import asyncio
from datetime import datetime

from app.core.logger import get_logger
from app.infrastructure.db import async_session_factory
from app.infrastructure.llm import LangChainEvaluationAnalyzer
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.evaluation_repository import EvaluationRepository
from app.repositories.job_repository import JobRepository
from app.models.evaluation import EvaluationStatus
from app.services.evaluation_service import EvaluationService

_processing_ids: set[int] = set()
_processing_lock = asyncio.Lock()
logger = get_logger(__name__)


async def _mark_failed(evaluation_id: int) -> None:
    """Best-effort fallback to mark an evaluation as failed."""
    async with async_session_factory() as session:
        repository = EvaluationRepository(session)
        evaluation = await repository.get_by_id(evaluation_id)
        if evaluation is None:
            return
        if evaluation.status == EvaluationStatus.COMPLETED.value:
            return
        await repository.update(
            evaluation,
            {
                "status": EvaluationStatus.FAILED.value,
                "completed_at": datetime.now(),
            },
        )
        await session.commit()


async def process_evaluation_job(evaluation_id: int) -> None:
    """Build runtime dependencies and process one evaluation asynchronously."""
    async with _processing_lock:
        if evaluation_id in _processing_ids:
            return
        _processing_ids.add(evaluation_id)

    try:
        async with async_session_factory() as session:
            repository = EvaluationRepository(session)
            candidate_repository = CandidateRepository(session)
            job_repository = JobRepository(session)
            try:
                analyzer = LangChainEvaluationAnalyzer()
            except Exception as exc:
                logger.exception(
                    "Failed to initialize evaluation analyzer",
                    exc_info=exc,
                )
                evaluation = await repository.get_by_id(evaluation_id)
                if evaluation is not None:
                    await repository.update(
                        evaluation,
                        {
                            "status": EvaluationStatus.FAILED.value,
                            "completed_at": datetime.now(),
                        },
                    )
                    await session.commit()
                return

            service = EvaluationService(
                repository,
                candidate_repository,
                job_repository,
                session,
                analyzer=analyzer,
            )
            await service.process_evaluation(evaluation_id)
    except Exception as exc:
        logger.exception("Unhandled background evaluation error", exc_info=exc)
        await _mark_failed(evaluation_id)
    finally:
        async with _processing_lock:
            _processing_ids.discard(evaluation_id)

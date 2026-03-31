import type { EvaluationRecord } from '@/domain/types'
import { mockEvaluationDashboardData } from '@/domain/mock-data'

/**
 * Obtiene una evaluación por candidato y puesto.
 * TODO: reemplazar por fetch(`/api/v1/evaluations?candidateId=${candidateId}&jobId=${jobId}`)
 */
export async function fetchEvaluation(
  candidateId: string,
  jobId: string,
): Promise<EvaluationRecord | undefined> {
  return mockEvaluationDashboardData.evaluations.find(
    (evaluation) =>
      evaluation.candidateId === candidateId && evaluation.jobId === jobId,
  )
}

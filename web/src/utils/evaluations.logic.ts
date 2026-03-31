import type { EvaluationRecord } from '@/domain/types'

/**
 * Busca una evaluación por candidato y puesto.
 */
export function findEvaluationByCandidateAndJob(
  evaluations: EvaluationRecord[],
  candidateId: string,
  jobId: string,
): EvaluationRecord | undefined {
  return evaluations.find(
    (evaluation) =>
      evaluation.candidateId === candidateId && evaluation.jobId === jobId,
  )
}

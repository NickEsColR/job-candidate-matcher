import type { Candidate } from '@/domain/types'
import { mockEvaluationDashboardData } from '@/domain/mock-data'

/**
 * Obtiene todos los candidatos.
 * TODO: reemplazar por fetch('/api/v1/candidates')
 */
export async function fetchCandidates(): Promise<Candidate[]> {
  return mockEvaluationDashboardData.candidates
}

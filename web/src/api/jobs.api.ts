import type { JobOpening } from '@/domain/types'
import { mockEvaluationDashboardData } from '@/domain/mock-data'

/**
 * Obtiene todas las vacantes.
 * TODO: reemplazar por fetch('/api/v1/jobs')
 */
export async function fetchJobs(): Promise<JobOpening[]> {
  return mockEvaluationDashboardData.jobs
}

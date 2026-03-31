import type { JobOpening } from '@/domain/types'
import { mutableJobs } from '@/domain/mock-data'

/**
 * Obtiene todas las vacantes.
 * TODO: reemplazar por fetch('/api/v1/jobs')
 */
export async function fetchJobs(): Promise<JobOpening[]> {
  return [...mutableJobs]
}

/**
 * Crea un nuevo puesto.
 * TODO: reemplazar por fetch('/api/v1/jobs', { method: 'POST', body: ... })
 */
export async function createJob(
  data: Omit<JobOpening, 'id'>,
): Promise<JobOpening> {
  const job: JobOpening = {
    ...data,
    id: `job-${Date.now()}`,
  }
  mutableJobs.push(job)
  return job
}

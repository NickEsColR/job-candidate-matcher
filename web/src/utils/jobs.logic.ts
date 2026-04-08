import type { JobOpening } from '@/domain/types'

/**
 * Busca una vacante por ID. Si no existe, devuelve la primera de la lista.
 */
export function findJobById(
  jobs: JobOpening[],
  id: string,
): JobOpening | undefined {
  return jobs.find((job) => job.id === id) ?? jobs[0]
}

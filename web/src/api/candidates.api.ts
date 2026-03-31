import type { Candidate } from '@/domain/types'
import { mutableCandidates } from '@/domain/mock-data'

/**
 * Obtiene todos los candidatos.
 * TODO: reemplazar por fetch('/api/v1/candidates')
 */
export async function fetchCandidates(): Promise<Candidate[]> {
  return [...mutableCandidates]
}

/**
 * Crea un nuevo candidato.
 * TODO: reemplazar por fetch('/api/v1/candidates', { method: 'POST', body: ... })
 */
export async function createCandidate(
  data: Omit<Candidate, 'id'>,
): Promise<Candidate> {
  const candidate: Candidate = {
    ...data,
    id: `candidate-${Date.now()}`,
  }
  mutableCandidates.push(candidate)
  return candidate
}

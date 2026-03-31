import type { Candidate } from '@/domain/types'

/**
 * Busca un candidato por ID. Si no existe, devuelve el primero de la lista.
 */
export function findCandidateById(
  candidates: Candidate[],
  id: string,
): Candidate | undefined {
  return candidates.find((candidate) => candidate.id === id) ?? candidates[0]
}

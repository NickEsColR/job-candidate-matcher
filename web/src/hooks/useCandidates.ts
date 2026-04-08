import { useState, useEffect, useCallback } from 'preact/hooks'
import { fetchCandidates, createCandidate } from '@/api/candidates.api'
import type { Candidate } from '@/domain/types'

interface UseCandidatesResult {
  candidates: Candidate[]
  loading: boolean
  error: string | null
  addCandidate: (data: Omit<Candidate, 'id'>) => Promise<Candidate>
}

export function useCandidates(): UseCandidatesResult {
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCandidates()
      .then(setCandidates)
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
      .finally(() => setLoading(false))
  }, [])

  const addCandidate = useCallback(
    async (data: Omit<Candidate, 'id'>) => {
      const candidate = await createCandidate(data)
      setCandidates((prev) => [...prev, candidate])
      return candidate
    },
    [],
  )

  return { candidates, loading, error, addCandidate }
}

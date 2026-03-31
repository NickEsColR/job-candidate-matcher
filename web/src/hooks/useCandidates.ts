import { useState, useEffect } from 'preact/hooks'
import { fetchCandidates } from '@/api/candidates.api'
import type { Candidate } from '@/domain/types'

interface UseCandidatesResult {
  candidates: Candidate[]
  loading: boolean
  error: string | null
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

  return { candidates, loading, error }
}

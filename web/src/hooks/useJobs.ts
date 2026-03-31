import { useState, useEffect } from 'preact/hooks'
import { fetchJobs } from '@/api/jobs.api'
import type { JobOpening } from '@/domain/types'

interface UseJobsResult {
  jobs: JobOpening[]
  loading: boolean
  error: string | null
}

export function useJobs(): UseJobsResult {
  const [jobs, setJobs] = useState<JobOpening[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchJobs()
      .then(setJobs)
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
      .finally(() => setLoading(false))
  }, [])

  return { jobs, loading, error }
}

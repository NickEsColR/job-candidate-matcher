import { useState, useEffect, useCallback } from 'preact/hooks'
import { fetchJobs, createJob } from '@/api/jobs.api'
import type { JobOpening } from '@/domain/types'

interface UseJobsResult {
  jobs: JobOpening[]
  loading: boolean
  error: string | null
  addJob: (data: Omit<JobOpening, 'id'>) => Promise<JobOpening>
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

  const addJob = useCallback(async (data: Omit<JobOpening, 'id'>) => {
    const job = await createJob(data)
    setJobs((prev) => [...prev, job])
    return job
  }, [])

  return { jobs, loading, error, addJob }
}

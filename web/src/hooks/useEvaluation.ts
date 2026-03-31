import { useState, useEffect } from 'preact/hooks'
import { fetchEvaluation } from '@/api/evaluations.api'
import type { EvaluationRecord } from '@/domain/types'

export type EvaluationStatus = 'loading' | 'completed' | 'error' | 'empty'

interface UseEvaluationResult {
  evaluation: EvaluationRecord | undefined
  status: EvaluationStatus
}

/**
 * Obtiene la evaluación para un candidato y puesto específicos.
 * Se ejecuta cuando cambian candidateId o jobId.
 */
export function useEvaluation(
  candidateId: string,
  jobId: string,
): UseEvaluationResult {
  const [evaluation, setEvaluation] = useState<EvaluationRecord | undefined>(undefined)
  const [status, setStatus] = useState<EvaluationStatus>('loading')

  useEffect(() => {
    if (!candidateId || !jobId) {
      setStatus('empty')
      setEvaluation(undefined)
      return
    }

    setStatus('loading')
    fetchEvaluation(candidateId, jobId)
      .then((result) => {
        if (!result) {
          setEvaluation(undefined)
          setStatus('empty')
          return
        }
        setEvaluation(result)
        setStatus(result.status === 'completed' ? 'completed' : 'error')
      })
      .catch(() => {
        setEvaluation(undefined)
        setStatus('error')
      })
  }, [candidateId, jobId])

  return { evaluation, status }
}

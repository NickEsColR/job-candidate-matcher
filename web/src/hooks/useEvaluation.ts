import { useState, useEffect, useCallback, useRef } from 'preact/hooks'
import { getEvaluation, createEvaluation } from '@/api/evaluations.api'
import type { EvaluationRecord } from '@/domain/types'

export type EvaluationHookStatus =
  | 'loading'
  | 'completed'
  | 'error'
  | 'in_progress'
  | 'empty'

interface UseEvaluationResult {
  evaluation: EvaluationRecord | undefined
  status: EvaluationHookStatus
  triggerEvaluation: () => Promise<void>
}

const POLL_INTERVAL_MS = 1500

/**
 * Gestiona el estado de una evaluación para un candidato y puesto.
 * - Carga inicial: consulta si ya existe una evaluación
 * - triggerEvaluation(): crea una nueva (o reintentar), hace polling hasta completed/error
 */
export function useEvaluation(
  candidateId: string,
  jobId: string,
): UseEvaluationResult {
  const [evaluation, setEvaluation] = useState<EvaluationRecord | undefined>(
    undefined,
  )
  const [status, setStatus] = useState<EvaluationHookStatus>('loading')
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  /** Limpia el intervalo de polling si existe */
  function stopPolling() {
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
  }

  /** Consulta el estado actual y actualiza el estado del hook */
  async function checkStatus(cId: string, jId: string) {
    const result = await getEvaluation(cId, jId)
    if (!result) {
      setEvaluation(undefined)
      setStatus('empty')
      return 'empty' as const
    }
    setEvaluation(result)
    setStatus(result.status)
    return result.status
  }

  /** Inicia polling hasta que el estado salga de in_progress */
  function startPolling(cId: string, jId: string) {
    stopPolling()
    pollRef.current = setInterval(async () => {
      const currentStatus = await checkStatus(cId, jId)
      if (currentStatus !== 'in_progress') {
        stopPolling()
      }
    }, POLL_INTERVAL_MS)
  }

  // Carga inicial: consultar evaluación existente al cambiar candidato/puesto
  useEffect(() => {
    stopPolling()

    if (!candidateId || !jobId) {
      setEvaluation(undefined)
      setStatus('empty')
      return
    }

    setStatus('loading')
    checkStatus(candidateId, jobId).then((currentStatus) => {
      if (currentStatus === 'in_progress') {
        startPolling(candidateId, jobId)
      }
    })

    return () => stopPolling()
  }, [candidateId, jobId])

  // Crear o reintentar evaluación
  const triggerEvaluation = useCallback(async () => {
    if (!candidateId || !jobId) return

    setStatus('in_progress')
    await createEvaluation(candidateId, jobId)
    startPolling(candidateId, jobId)
  }, [candidateId, jobId])

  return { evaluation, status, triggerEvaluation }
}

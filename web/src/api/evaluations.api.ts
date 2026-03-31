import type { EvaluationRecord, CompletedEvaluation } from '@/domain/types'
import { mockEvaluationDashboardData } from '@/domain/mock-data'

/**
 * Store mutable de evaluaciones compartido con los hooks.
 * Simula el estado del backend.
 */
const mutableEvaluations: EvaluationRecord[] = [
  ...mockEvaluationDashboardData.evaluations,
]

/**
 * Obtiene una evaluación por candidato y puesto.
 * TODO: reemplazar por fetch(`/api/v1/evaluations?candidateId=...&jobId=...`)
 */
export async function getEvaluation(
  candidateId: string,
  jobId: string,
): Promise<EvaluationRecord | undefined> {
  return mutableEvaluations.find(
    (e) => e.candidateId === candidateId && e.jobId === jobId,
  )
}

/**
 * Crea una nueva evaluación. Devuelve inmediatamente con estado in_progress.
 * El backend mock procesa en background y cambia a completed o error.
 * TODO: reemplazar por fetch('/api/v1/evaluations', { method: 'POST', body: ... })
 */
export async function createEvaluation(
  candidateId: string,
  jobId: string,
): Promise<EvaluationRecord> {
  // Eliminar evaluación previa si existe (reintento)
  const existingIdx = mutableEvaluations.findIndex(
    (e) => e.candidateId === candidateId && e.jobId === jobId,
  )
  if (existingIdx !== -1) {
    mutableEvaluations.splice(existingIdx, 1)
  }

  const evaluation: EvaluationRecord = {
    id: `eval-${Date.now()}`,
    candidateId,
    jobId,
    status: 'in_progress',
  }

  mutableEvaluations.push(evaluation)

  // Mock: procesar en background (simula latencia del backend)
  mockProcessEvaluation(evaluation.id)

  return { ...evaluation }
}

/**
 * Mock del procesamiento del backend.
 * Después de un delay, cambia la evaluación a completed o error.
 */
function mockProcessEvaluation(evaluationId: string): void {
  const delay = 2000 + Math.random() * 3000 // 2-5 segundos

  setTimeout(() => {
    const evaluation = mutableEvaluations.find((e) => e.id === evaluationId)
    if (!evaluation) return

    // 80% completed, 20% error (simula fallos ocasionales)
    const isCompleted = Math.random() > 0.2

    if (isCompleted) {
      evaluation.status = 'completed'
      evaluation.completedEvaluation = generateMockResult()
    } else {
      evaluation.status = 'error'
    }
  }, delay)
}

/**
 * Genera un resultado mock de evaluación completada.
 */
function generateMockResult(): CompletedEvaluation {
  const score = Math.floor(60 + Math.random() * 40) // 60-99

  return {
    score,
    maxScore: 100,
    executiveSummary:
      'El candidato muestra una sólida comprensión de los requisitos técnicos del puesto. Su experiencia previa en entornos de alta demanda demuestra capacidad de adaptación y resolución de problemas complejos. Se recomienda avanzar a la siguiente etapa del proceso de selección.',
    strengths: [
      'Excelente capacidad de comunicación técnica',
      'Sólida experiencia en arquitectura de sistemas distribuidos',
      'Proactividad en la resolución de incidencias críticas',
    ],
    improvementAreas: [
      'Podría profundizar en frameworks de observabilidad',
      'Documentación técnica podría ser más detallada',
    ],
    finalRecommendations: [
      'Proceder con entrevista técnica avanzada',
      'Validar compatibilidad cultural con el equipo',
      'Considerar para programa de mentoría senior',
    ],
  }
}

import type { Candidate, DashboardData } from '@/domain/types'

export const mockEvaluationDashboardData: DashboardData = {
  candidates: [
    {
      id: 'candidate-1',
      name: 'Adrian Villalobos',
      email: 'a.villalobos@example.com',
      yearsOfExperience: 8,
      resumeUrl: '#',
      skills: ['Arquitectura de Datos', 'Python Senior', 'Cloud Ops'],
    },
    {
      id: 'candidate-2',
      name: 'Mariana Estévez',
      email: 'm.estevez@example.com',
      yearsOfExperience: 6,
      resumeUrl: '#',
      skills: ['Machine Learning', 'MLOps', 'Data Engineering'],
    },
    {
      id: 'candidate-3',
      name: 'Carlos Ruiz',
      email: 'c.ruiz@example.com',
      yearsOfExperience: 10,
      resumeUrl: '#',
      skills: ['Arquitectura Cloud', 'Kubernetes', 'DevSecOps'],
    },
  ],
  jobs: [
    {
      id: 'job-1',
      title: 'Arquitecto de Soluciones Cloud',
      summary:
        'Buscamos un líder técnico capaz de diseñar infraestructuras escalables y seguras en entornos multi-cloud.',
      requirements: [
        { id: 'req-1', label: 'Certificación AWS Solution Architect' },
        { id: 'req-2', label: 'Experiencia con Kubernetes/Docker' },
      ],
      location: 'Remoto (LATAM)',
      salaryRange: '$5.5k - $7.2k USD',
    },
    {
      id: 'job-2',
      title: 'Senior Frontend Engineer',
      summary:
        'Responsable de construir experiencias de usuario de alto impacto con foco en performance y accesibilidad.',
      requirements: [
        { id: 'req-3', label: 'Experiencia avanzada en TypeScript y React/Preact' },
        { id: 'req-4', label: 'Dominio de arquitectura frontend escalable' },
      ],
      location: 'Híbrido (CDMX)',
      salaryRange: '$4.8k - $6.3k USD',
    },
    {
      id: 'job-3',
      title: 'Data Scientist Lead',
      summary:
        'Liderará el diseño de modelos predictivos y su puesta en producción para resolver retos de negocio complejos.',
      requirements: [
        { id: 'req-5', label: 'Experiencia liderando equipos de ciencia de datos' },
        { id: 'req-6', label: 'Experiencia en despliegue de modelos en producción' },
      ],
      location: 'Remoto (Global)',
      salaryRange: '$6.0k - $8.0k USD',
    },
  ],
  evaluations: [
    {
      id: 'evaluation-1',
      candidateId: 'candidate-1',
      jobId: 'job-1',
      status: 'completed',
      completedEvaluation: {
        score: 85,
        maxScore: 100,
        executiveSummary:
          'El candidato demuestra un dominio excepcional de las arquitecturas distribuidas. Su capacidad para articular soluciones complejas de manera simplificada durante la prueba técnica sugiere una alta aptitud para el liderazgo de equipos y la comunicación con stakeholders.',
        strengths: [
          'Resolución proactiva de cuellos de botella en DB.',
          'Excelentes prácticas de seguridad (DevSecOps).',
          'Mentalidad orientada a la optimización de costes.',
        ],
        improvementAreas: [
          'Profundizar en frameworks de IA generativa.',
          'Documentación técnica un poco escueta.',
        ],
        finalRecommendations: [
          'Proceder a la fase de entrevista con el CTO.',
          'Considerar para el programa de bonos por expertise.',
          'Asignar un mentor de Onboarding para cultura interna.',
          'Validar expectativas de reubicación si aplica.',
        ],
      },
    },
    {
      id: 'evaluation-2',
      candidateId: 'candidate-3',
      jobId: 'job-3',
      status: 'error',
    },
    {
      id: 'evaluation-3',
      candidateId: 'candidate-2',
      jobId: 'job-2',
      status: 'error',
    },
  ],
}

/**
 * Array mutable de candidatos compartido con la capa API.
 * La API escribe aquí; los hooks leen copias.
 * Para cambiar a API real: reemplazar fetchCandidates/createCandidate
 * en candidates.api.ts por fetch() — este array se ignora.
 */
export const mutableCandidates: Candidate[] = [
  ...mockEvaluationDashboardData.candidates,
]

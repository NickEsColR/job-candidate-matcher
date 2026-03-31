export interface Candidate {
  id: string
  name: string
  email: string
  yearsOfExperience: number
  resumeUrl: string
  skills: string[]
}

export interface JobRequirement {
  id: string
  label: string
}

export interface JobOpening {
  id: string
  title: string
  summary: string
  requirements: JobRequirement[]
  location: string
  salaryRange: string
}

export interface CompletedEvaluation {
  score: number
  maxScore: number
  executiveSummary: string
  strengths: string[]
  improvementAreas: string[]
  finalRecommendations: string[]
}

export type EvaluationStatus = 'completed' | 'error' | 'in_progress'

export interface EvaluationRecord {
  id: string
  candidateId: string
  jobId: string
  status: EvaluationStatus
  completedEvaluation?: CompletedEvaluation
}

export interface DashboardData {
  candidates: Candidate[]
  jobs: JobOpening[]
  evaluations: EvaluationRecord[]
}

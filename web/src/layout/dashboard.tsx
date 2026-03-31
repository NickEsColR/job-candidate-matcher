import { useState, useEffect } from 'preact/hooks'
import { CandidateCard } from '@/cards/candidate-card'
import { EvaluationCard } from '@/cards/evaluation-card'
import { JobCard } from '@/cards/job-card'
import { EvaluationStateCard } from '@/cards/evaluation-state-card'
import { EvaluationSkeleton } from '@/cards/evaluation-skeleton'
import { Footer } from './footer'
import { Header } from './header'
import { CreateCandidateModal } from './create-candidate-modal'
import { useCandidates } from '@/hooks/useCandidates'
import { useJobs } from '@/hooks/useJobs'
import { useEvaluation } from '@/hooks/useEvaluation'
import { findCandidateById } from '@/utils/candidates.logic'
import { findJobById } from '@/utils/jobs.logic'

export function Dashboard() {
  const { candidates, addCandidate } = useCandidates()
  const { jobs } = useJobs()
  const [isModalOpen, setIsModalOpen] = useState(false)

  const [selectedCandidateId, setSelectedCandidateId] = useState('')
  const [selectedJobId, setSelectedJobId] = useState('')

  // Auto-seleccionar el primer candidato y job cuando llega la data
  useEffect(() => {
    if (!selectedCandidateId && candidates.length > 0) {
      setSelectedCandidateId(candidates[0].id)
    }
  }, [candidates, selectedCandidateId])

  useEffect(() => {
    if (!selectedJobId && jobs.length > 0) {
      setSelectedJobId(jobs[0].id)
    }
  }, [jobs, selectedJobId])

  const { evaluation, status: evaluationStatus } = useEvaluation(
    selectedCandidateId,
    selectedJobId,
  )

  const selectedCandidate = findCandidateById(candidates, selectedCandidateId)
  const selectedJob = findJobById(jobs, selectedJobId)

  const evaluationSection = (() => {
    if (evaluationStatus === 'loading') return <EvaluationSkeleton />

    if (evaluationStatus === 'completed' && evaluation) {
      return <EvaluationCard evaluation={evaluation.completedEvaluation!} />
    }

    if (evaluationStatus === 'error') return <EvaluationStateCard variant="error" />

    return <EvaluationStateCard variant="empty" />
  })()

  return (
    <div class="min-h-screen bg-background font-sans text-on-background">
      <Header onCreateCandidate={() => setIsModalOpen(true)} />

      <main class="mx-auto max-w-screen-2xl px-8 pt-32 pb-20 max-md:px-5">
        <div class="grid grid-cols-12 gap-8">
          <div class="col-span-12 lg:col-span-6">
            <CandidateCard
              candidates={candidates}
              selectedCandidate={selectedCandidate}
              onCandidateChange={setSelectedCandidateId}
            />
          </div>

          <div class="col-span-12 lg:col-span-6">
            <JobCard
              jobs={jobs}
              selectedJob={selectedJob}
              onJobChange={setSelectedJobId}
            />
          </div>

          <div class="col-span-12">{evaluationSection}</div>
        </div>
      </main>

      <Footer />

      {isModalOpen && (
        <CreateCandidateModal
          onClose={() => setIsModalOpen(false)}
          onCreate={addCandidate}
        />
      )}
    </div>
  )
}

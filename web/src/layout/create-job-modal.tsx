import { useState } from 'preact/hooks'
import type { JobOpening } from '@/domain/types'
import type { JobFormData } from '@/utils/job-form.schema'
import {
  addRequirementToCurrentRequirements,
  removeRequirementFromCurrentRequirements,
  validateJobForm,
  prepareJobForSubmission,
} from '@/utils/job-form.logic'

interface CreateJobModalProps {
  onClose: () => void
  onCreate: (job: Omit<JobOpening, 'id'>) => Promise<JobOpening>
}

export function CreateJobModal({ onClose, onCreate }: CreateJobModalProps) {
  const [title, setTitle] = useState('')
  const [summary, setSummary] = useState('')
  const [requirements, setRequirements] = useState<string[]>([])
  const [requirementInput, setRequirementInput] = useState('')
  const [location, setLocation] = useState('')
  const [salaryRange, setSalaryRange] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [saving, setSaving] = useState(false)

  function addRequirement() {
    const { newRequirements, inputCleared } =
      addRequirementToCurrentRequirements(requirements, requirementInput)
    if (inputCleared) {
      setRequirements(newRequirements)
      setRequirementInput('')
      setErrors((prev) => {
        const next = { ...prev }
        delete next.requirements
        return next
      })
    }
  }

  function removeRequirement(requirement: string) {
    setRequirements(
      removeRequirementFromCurrentRequirements(requirements, requirement),
    )
  }

  function handleRequirementKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      e.preventDefault()
      addRequirement()
    }
  }

  async function handleSubmit(e: Event) {
    e.preventDefault()
    setErrors({})

    const raw: JobFormData = {
      title,
      summary,
      requirements,
      location,
      salaryRange,
    }

    const validation = validateJobForm(raw)

    if (!validation.success) {
      setErrors(validation.errors)
      return
    }

    setSaving(true)
    try {
      const jobData = prepareJobForSubmission(validation.data)
      await onCreate(jobData)
      onClose()
    } finally {
      setSaving(false)
    }
  }

  return (
    <div
      class="fixed inset-0 z-[60] flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="create-job-title"
    >
      {/* Backdrop */}
      <div
        class="absolute inset-0 bg-background/60 backdrop-blur-md"
        onClick={onClose}
      />

      {/* Modal Content */}
      <div class="relative backdrop-blur-md w-full max-w-2xl overflow-hidden rounded-xl border border-outline-variant/20 bg-surface-container-low shadow-2xl">
        <div class="p-8">
          <div class="mb-8 flex items-start justify-between">
            <div>
              <h1
                id="create-job-title"
                class="text-2xl font-bold tracking-tight text-primary"
              >
                Crear Puesto
              </h1>
              <p class="mt-1 text-sm text-on-surface-variant">
                Ingrese los detalles para la nueva vacante.
              </p>
            </div>
            <button
              class="material-symbols-outlined text-on-surface-variant transition-colors hover:text-on-surface"
              onClick={onClose}
              type="button"
              aria-label="Cerrar modal"
            >
              close
            </button>
          </div>

          <form class="space-y-6" onSubmit={handleSubmit}>
            {/* Title Field */}
            <div class="space-y-2">
              <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                Título del Puesto <span class="text-error">*</span>
              </label>
              <input
                class="w-full rounded-lg border-none bg-surface-container p-3 text-on-surface placeholder:text-on-surface-variant/30 transition-all focus:ring-2 focus:ring-primary/40"
                placeholder="Ej. Arquitecto de Soluciones Cloud"
                type="text"
                value={title}
                onInput={(e) => {
                  setTitle((e.currentTarget as HTMLInputElement).value)
                  setErrors((prev) => {
                    const next = { ...prev }
                    delete next.title
                    return next
                  })
                }}
              />
              {errors.title && (
                <p class="text-xs text-error">{errors.title}</p>
              )}
            </div>

            {/* Summary Field */}
            <div class="space-y-2">
              <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                Resumen <span class="text-error">*</span>
              </label>
              <textarea
                class="w-full rounded-lg border-none bg-surface-container p-3 text-on-surface placeholder:text-on-surface-variant/30 transition-all focus:ring-2 focus:ring-primary/40"
                placeholder="Describa las responsabilidades principales del puesto..."
                rows={3}
                value={summary}
                onInput={(e) => {
                  setSummary((e.currentTarget as HTMLTextAreaElement).value)
                  setErrors((prev) => {
                    const next = { ...prev }
                    delete next.summary
                    return next
                  })
                }}
              />
              {errors.summary && (
                <p class="text-xs text-error">{errors.summary}</p>
              )}
            </div>

            {/* Requirements List */}
            <div class="space-y-3">
              <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                Requisitos <span class="text-error">*</span>
              </label>
              <div class="flex min-h-12 flex-wrap items-center gap-2 rounded-lg bg-surface-container p-3">
                {requirements.map((req) => (
                  <span
                    key={req}
                    class="flex items-center gap-2 rounded-md bg-secondary-container px-3 py-1 text-sm text-on-secondary-container"
                  >
                    {req}
                    <button
                      class="material-symbols-outlined text-[16px]"
                      onClick={() => removeRequirement(req)}
                      type="button"
                      aria-label={`Eliminar requisito: ${req}`}
                    >
                      close
                    </button>
                  </span>
                ))}
                <input
                  class="w-32 border-none bg-transparent py-1 text-sm placeholder:text-on-surface-variant/30 focus:ring-0"
                  placeholder="Añadir..."
                  type="text"
                  value={requirementInput}
                  onInput={(e) =>
                    setRequirementInput(
                      (e.currentTarget as HTMLInputElement).value,
                    )
                  }
                  onKeyDown={handleRequirementKeyDown}
                  onBlur={addRequirement}
                />
              </div>
              {errors.requirements && (
                <p class="text-xs text-error">{errors.requirements}</p>
              )}
            </div>

            <div class="grid grid-cols-2 gap-6">
              {/* Location Field */}
              <div class="space-y-2">
                <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                  Ubicación
                </label>
                <input
                  class="w-full rounded-lg border-none bg-surface-container p-3 text-on-surface placeholder:text-on-surface-variant/30 transition-all focus:ring-2 focus:ring-primary/40"
                  placeholder="Ej. Remoto (LATAM)"
                  type="text"
                  value={location}
                  onInput={(e) =>
                    setLocation((e.currentTarget as HTMLInputElement).value)
                  }
                />
              </div>

              {/* Salary Range Field */}
              <div class="space-y-2">
                <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                  Rango Salarial
                </label>
                <input
                  class="w-full rounded-lg border-none bg-surface-container p-3 text-on-surface placeholder:text-on-surface-variant/30 transition-all focus:ring-2 focus:ring-primary/40"
                  placeholder="Ej. $5.5k - $7.2k USD"
                  type="text"
                  value={salaryRange}
                  onInput={(e) =>
                    setSalaryRange((e.currentTarget as HTMLInputElement).value)
                  }
                />
              </div>
            </div>

            {/* Footer Actions */}
            <div class="mt-8 flex justify-end gap-4 border-t border-outline-variant/10 pt-6">
              <button
                class="rounded-full px-6 py-2.5 font-medium text-on-surface-variant transition-all hover:bg-surface-container hover:text-on-surface"
                onClick={onClose}
                type="button"
              >
                Cancelar
              </button>
              <button
                class="flex items-center gap-2 rounded-full bg-primary-container px-8 py-2.5 font-bold text-white shadow-lg shadow-primary-container/20 transition-all hover:bg-inverse-primary disabled:opacity-50"
                disabled={saving}
                type="submit"
              >
                <span class="material-symbols-outlined text-[20px]">save</span>
                {saving ? 'Guardando...' : 'Guardar Puesto'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

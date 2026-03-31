import type { JobOpening } from "@/domain/types";

interface JobCardProps {
  jobs: JobOpening[];
  selectedJob: JobOpening | undefined;
  onJobChange: (jobId: string) => void;
}

export function JobCard({ jobs, selectedJob, onJobChange }: JobCardProps) {
  if (!selectedJob) {
    return (
      <section
        class="flex flex-col gap-6 rounded-3xl border border-outline-variant/10 bg-surface-container-low p-8 shadow-lg"
        aria-labelledby="job-opening-title"
      >
        <header>
          <span class="text-xs font-bold tracking-widest text-tertiary uppercase">
            Posición Abierta
          </span>
          <h2
            id="job-opening-title"
            class="mt-2 mb-0 text-3xl font-bold text-on-surface"
          >
            Título del Puesto
          </h2>
        </header>

        <p class="m-0 text-base text-on-surface-variant">
          No hay vacantes disponibles.
        </p>
      </section>
    );
  }

  return (
    <section
      class="flex flex-col gap-6 rounded-3xl border border-outline-variant/10 bg-surface-container-low p-8 shadow-lg"
      aria-labelledby="job-opening-title"
    >
      <header>
        <span class="text-xs font-bold tracking-widest text-tertiary uppercase">
          Posición Abierta
        </span>
        <h2
          id="job-opening-title"
          class="mt-2 mb-0 text-3xl font-bold text-on-surface"
        >
          {selectedJob.title}
        </h2>
      </header>

      <div class="flex flex-col gap-4">
        <label
          class="text-sm font-medium text-on-surface-variant"
          for="job-select"
        >
          Cambiar Vacante
        </label>
        <div class="relative">
          <select
            id="job-select"
            class="w-full appearance-none rounded-xl border-0 bg-surface-container px-4 py-3 pr-12 text-base text-on-surface focus:outline-2 focus:outline-tertiary/40"
            value={selectedJob.id}
            onInput={(event) => {
              const jobId = (event.currentTarget as HTMLSelectElement).value;
              onJobChange(jobId);
            }}
          >
            {jobs.map((job) => (
              <option key={job.id} value={job.id}>
                {job.title}
              </option>
            ))}
          </select>
          <span
            class="material-symbols-outlined pointer-events-none absolute top-3 right-4 text-outline"
            aria-hidden="true"
          >
            expand_more
          </span>
        </div>
      </div>

      <div class="flex flex-col gap-5">
        <div>
          <p class="mt-0 mb-3 text-sm font-semibold text-on-surface-variant">
            Resumen
          </p>
          <p class="m-0 text-sm leading-relaxed text-on-surface-variant">
            {selectedJob.summary}
          </p>
        </div>

        <div>
          <p class="mt-0 mb-3 text-sm font-semibold text-on-surface-variant">
            Requisitos Principales
          </p>
          <ul class="m-0 flex list-none flex-col gap-2 p-0 text-sm text-on-surface-variant">
            {selectedJob.requirements.map((requirement) => (
              <li key={requirement.id} class="flex items-center gap-2 italic">
                <span
                  class="material-symbols-outlined text-sm text-tertiary"
                  aria-hidden="true"
                >
                  check_circle
                </span>
                {requirement.label}
              </li>
            ))}
          </ul>
        </div>

        <div class="grid grid-cols-2 gap-4 border-t border-outline-variant/20 pt-4 max-md:grid-cols-1">
          <div>
            <p class="m-0 text-xs font-bold tracking-wide text-outline uppercase">
              Ubicación
            </p>
            <p class="mt-1 mb-0 text-sm font-bold text-on-surface">
              {selectedJob.location}
            </p>
          </div>
          <div>
            <p class="m-0 text-xs font-bold tracking-wide text-outline uppercase">
              Rango Salarial
            </p>
            <p class="mt-1 mb-0 text-sm font-bold text-on-surface">
              {selectedJob.salaryRange}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

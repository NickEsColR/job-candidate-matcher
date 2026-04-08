import type { Candidate } from "@/domain/types";

interface CandidateCardProps {
  candidates: Candidate[];
  selectedCandidate: Candidate | undefined;
  onCandidateChange: (candidateId: string) => void;
}

export function CandidateCard({
  candidates,
  selectedCandidate,
  onCandidateChange,
}: CandidateCardProps) {
  if (!selectedCandidate) {
    return (
      <section
        class="flex flex-col gap-6 rounded-3xl border border-outline-variant/10 bg-surface-container-low p-8 shadow-lg"
        aria-labelledby="candidate-profile-title"
      >
        <header>
          <span class="text-xs font-bold tracking-widest text-primary uppercase">
            Perfil del Talento
          </span>
          <h2
            id="candidate-profile-title"
            class="mt-2 mb-0 text-3xl font-bold text-on-surface"
          >
            Nombre del Candidato
          </h2>
        </header>

        <p class="m-0 text-base text-on-surface-variant">
          No hay candidatos disponibles.
        </p>
      </section>
    );
  }

  return (
    <section
      class="flex flex-col gap-6 rounded-3xl border border-outline-variant/10 bg-surface-container-low p-8 shadow-lg"
      aria-labelledby="candidate-profile-title"
    >
      <header>
        <span class="text-xs font-bold tracking-widest text-primary uppercase">
          Perfil del Talento
        </span>
        <h2
          id="candidate-profile-title"
          class="mt-2 mb-0 text-3xl font-bold text-on-surface"
        >
          {selectedCandidate.name}
        </h2>
      </header>

      <div class="flex flex-col gap-4">
        <label
          class="text-sm font-medium text-on-surface-variant"
          for="candidate-select"
        >
          Seleccionar Candidato
        </label>
        <div class="relative">
          <select
            id="candidate-select"
            class="w-full appearance-none rounded-xl border-0 bg-surface-container px-4 py-3 pr-12 text-base text-on-surface focus:outline-2 focus:outline-primary/40"
            value={selectedCandidate.id}
            onInput={(event) => {
              const candidateId = (event.currentTarget as HTMLSelectElement)
                .value;
              onCandidateChange(candidateId);
            }}
          >
            {candidates.map((candidate) => (
              <option key={candidate.id} value={candidate.id}>
                {candidate.name}
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

      <div class="flex flex-col gap-6 pt-4">
        <div class="flex items-center gap-3 text-on-surface-variant">
          <span
            class="material-symbols-outlined text-primary"
            aria-hidden="true"
          >
            mail
          </span>
          <span>{selectedCandidate.email}</span>
        </div>

        <div>
          <p class="mt-0 mb-3 text-sm font-semibold text-on-surface-variant">
            Habilidades Clave
          </p>
          <div class="flex flex-wrap gap-2">
            {selectedCandidate.skills.map((skill) => (
              <span
                key={skill}
                class="rounded-lg bg-secondary-container px-3 py-1 text-xs font-medium text-on-secondary-container"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div class="flex items-center justify-between border-t border-outline-variant/20 pt-4 max-md:flex-col max-md:items-start max-md:gap-4">
          <div>
            <p class="m-0 text-xs font-bold tracking-wide text-outline uppercase">
              Experiencia
            </p>
            <p class="mt-1 mb-0 text-2xl font-bold text-on-surface">
              {selectedCandidate.yearsOfExperience} años
            </p>
          </div>
          <a
            href={selectedCandidate.resumeUrl}
            class="inline-flex items-center gap-2 font-semibold text-primary no-underline hover:underline"
          >
            Ver Currículum
            <span
              class="material-symbols-outlined text-base"
              aria-hidden="true"
            >
              open_in_new
            </span>
          </a>
        </div>
      </div>
    </section>
  );
}

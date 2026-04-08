import type { CompletedEvaluation } from "@/domain/types";

interface EvaluationCardProps {
  evaluation: CompletedEvaluation;
  onGenerateReport?: () => void;
}

export function EvaluationCard({
  evaluation,
  onGenerateReport,
}: EvaluationCardProps) {
  return (
    <section
      class="rounded-3xl border border-outline-variant/20 bg-linear-to-r from-eval-gradient-start to-eval-gradient-end p-11 shadow-2xl max-md:p-6"
      aria-label="Evaluación completada"
    >
      <header class="flex justify-between gap-6 max-md:flex-col">
        <div>
          <span class="mb-3 inline-block text-xs font-bold tracking-widest text-primary uppercase">
            Métricas de Rendimiento
          </span>

          <div class="flex items-end gap-2.5">
            <p class="m-0 text-7xl leading-none font-extrabold tracking-tight text-primary md:text-8xl">
              {evaluation.score}
            </p>
            <p class="mb-2 text-4xl font-medium text-score-max max-md:mb-1 max-md:text-3xl">
              / {evaluation.maxScore}
            </p>
          </div>

          <p class="mt-2 mb-0 text-sm text-on-surface">
            Puntuación de la Evaluación
          </p>
        </div>

        <div class="flex min-w-60 flex-col items-end gap-3 max-md:min-w-0 max-md:items-start">
          <span class="inline-flex items-center gap-2 rounded-full bg-primary-container px-4 py-2.5 text-sm font-bold tracking-wide text-on-primary-container">
            <span class="material-symbols-outlined" aria-hidden="true">
              verified
            </span>
            COMPLETADO
          </span>

          <button
            type="button"
            class="cursor-pointer rounded-full border border-primary-fixed/45 bg-primary-fixed px-5 py-2.5 text-sm font-bold text-on-primary-fixed-variant"
            onClick={onGenerateReport}
          >
            Generar Reporte PDF
          </button>
        </div>
      </header>

      <div class="mt-10">
        <h3 class="mt-0 mb-3 text-3xl font-bold text-on-surface">
          Resumen Ejecutivo
        </h3>
        <p class="m-0 text-base leading-relaxed text-on-background">
          {evaluation.executiveSummary}
        </p>
      </div>

      <div class="mt-7 grid grid-cols-2 gap-7 max-md:grid-cols-1">
        <section>
          <h4 class="mb-3.5 flex items-center gap-2 text-base font-bold tracking-wide text-primary-fixed uppercase">
            <span class="material-symbols-outlined" aria-hidden="true">
              trending_up
            </span>
            Fortalezas
          </h4>

          <ul class="m-0 flex list-none flex-col gap-2.5 p-0">
            {evaluation.strengths.map((strength) => (
              <li
                key={strength}
                class="rounded-full border-l-2 border-l-primary bg-surface-container px-4 py-3 text-base text-on-background"
              >
                {strength}
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h4 class="mb-3.5 flex items-center gap-2 text-base font-bold tracking-wide text-tertiary uppercase">
            <span class="material-symbols-outlined" aria-hidden="true">
              warning
            </span>
            Áreas de Mejora
          </h4>

          <ul class="m-0 flex list-none flex-col gap-2.5 p-0">
            {evaluation.improvementAreas.map((area) => (
              <li
                key={area}
                class="rounded-full border-l-2 border-l-tertiary bg-surface-container px-4 py-3 text-base text-on-background"
              >
                {area}
              </li>
            ))}
          </ul>
        </section>
      </div>

      <section class="mt-7 rounded-3xl border border-outline-variant/35 bg-surface-container/85 p-6">
        <h4 class="mt-0 mb-3.5 flex items-center gap-2 text-base text-on-primary-container">
          <span class="material-symbols-outlined" aria-hidden="true">
            lightbulb
          </span>
          Recomendaciones Finales
        </h4>

        <ul class="m-0 columns-2 pl-5 text-sm leading-relaxed text-on-background max-md:columns-1">
          {evaluation.finalRecommendations.map((recommendation) => (
            <li key={recommendation} class="mb-1 break-inside-avoid">
              {recommendation}
            </li>
          ))}
        </ul>
      </section>
    </section>
  );
}

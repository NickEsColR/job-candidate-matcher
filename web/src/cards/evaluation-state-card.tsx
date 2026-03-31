type EvaluationVariant = 'empty' | 'error'

interface EvaluationStateCardProps {
  variant: EvaluationVariant
  onAction?: () => void
}

const CONTENT = {
  empty: {
    tag: 'Métricas de Rendimiento',
    icon: 'assignment_late',
    title: 'No hay evaluación',
    description:
      'Aún no se ha realizado un análisis técnico para este candidato en esta posición. Inicia el proceso para generar un reporte detallado de habilidades, fortalezas y áreas de mejora.',
    actionLabel: 'Iniciar Nueva Evaluación',
    actionIcon: 'play_arrow',
  },
  error: {
    tag: 'Métricas de Rendimiento',
    icon: 'error',
    title: 'Error en la Evaluación',
    description:
      'Hubo un problema técnico al procesar los datos de la evaluación. Por favor, intenta de nuevo o contacta al equipo de soporte si el error persiste.',
    actionLabel: 'Reintentar Evaluación',
    actionIcon: 'refresh',
  },
} as const

export function EvaluationStateCard({ variant, onAction }: EvaluationStateCardProps) {
  const isError = variant === 'error'
  const content = CONTENT[variant]

  const containerClass = isError
    ? 'relative overflow-hidden rounded-3xl border border-error/10 bg-surface-container p-10 shadow-2xl'
    : 'relative overflow-hidden rounded-3xl border border-outline-variant/10 bg-surface-container p-10 shadow-2xl'

  const glowClass = isError
    ? 'absolute -top-24 -right-24 h-64 w-64 rounded-full bg-error/5 blur-3xl'
    : 'absolute -top-24 -right-24 h-64 w-64 rounded-full bg-primary/5 blur-3xl'

  const iconWrapClass = isError
    ? 'mb-8 flex h-20 w-20 items-center justify-center rounded-3xl border border-error/20 bg-error-container/20'
    : 'mb-8 flex h-20 w-20 items-center justify-center rounded-3xl border border-outline-variant/20 bg-surface-container-high'

  const iconClass = isError
    ? 'material-symbols-outlined text-4xl text-error'
    : 'material-symbols-outlined text-4xl text-primary'

  const tagClass = isError
    ? 'mb-4 text-xs font-bold tracking-widest text-error uppercase'
    : 'mb-4 text-xs font-bold tracking-widest text-primary uppercase'

  const actionClass = isError
    ? 'inline-flex items-center gap-3 rounded-full border border-outline-variant bg-surface-container-highest px-10 py-4 text-base font-bold text-on-surface transition-all duration-300 hover:brightness-110 active:scale-95'
    : 'inline-flex items-center gap-3 rounded-full border-0 bg-primary px-10 py-4 text-base font-bold text-on-primary transition-all duration-300 hover:shadow-lg active:scale-95'

  return (
    <section class={containerClass}>
      <div class={glowClass} aria-hidden="true"></div>

      <div class="relative z-10 mx-auto flex min-h-96 max-w-3xl flex-col items-center justify-center text-center">
        <div class={iconWrapClass}>
          <span class={iconClass} aria-hidden="true">
            {content.icon}
          </span>
        </div>

        <span class={tagClass}>{content.tag}</span>

        <h2 class="mt-0 mb-4 text-4xl font-black tracking-tight text-on-surface">
          {content.title}
        </h2>
        <p class="mt-0 mb-10 text-xl leading-relaxed text-on-surface-variant max-md:text-base">
          {content.description}
        </p>

        <button type="button" class={actionClass} onClick={onAction}>
          <span class="material-symbols-outlined" aria-hidden="true">
            {content.actionIcon}
          </span>
          {content.actionLabel}
        </button>
      </div>
    </section>
  )
}

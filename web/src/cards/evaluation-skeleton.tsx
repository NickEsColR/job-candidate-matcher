/**
 * Skeleton de carga para la evaluación.
 * Se muestra mientras se obtiene la evaluación del backend.
 */
export function EvaluationSkeleton() {
  return (
    <section class="relative overflow-hidden rounded-3xl border border-outline-variant/10 bg-surface-container p-10 shadow-2xl">
      <div class="relative z-10 mx-auto flex min-h-96 max-w-3xl flex-col gap-8">
        {/* Header skeleton */}
        <div class="flex justify-between gap-6">
          <div class="flex flex-col gap-4">
            <div class="h-4 w-40 animate-pulse rounded-lg bg-surface-container-high" />
            <div class="h-20 w-48 animate-pulse rounded-lg bg-surface-container-high" />
          </div>
          <div class="flex flex-col items-end gap-3">
            <div class="h-10 w-32 animate-pulse rounded-full bg-surface-container-high" />
            <div class="h-10 w-44 animate-pulse rounded-full bg-surface-container-high" />
          </div>
        </div>

        {/* Summary skeleton */}
        <div class="flex flex-col gap-3">
          <div class="h-6 w-52 animate-pulse rounded-lg bg-surface-container-high" />
          <div class="h-4 w-full animate-pulse rounded-lg bg-surface-container-high" />
          <div class="h-4 w-3/4 animate-pulse rounded-lg bg-surface-container-high" />
        </div>

        {/* Columns skeleton */}
        <div class="grid grid-cols-2 gap-7 max-md:grid-cols-1">
          <div class="flex flex-col gap-3">
            <div class="h-5 w-28 animate-pulse rounded-lg bg-surface-container-high" />
            <div class="h-12 w-full animate-pulse rounded-full bg-surface-container-high" />
            <div class="h-12 w-full animate-pulse rounded-full bg-surface-container-high" />
            <div class="h-12 w-full animate-pulse rounded-full bg-surface-container-high" />
          </div>
          <div class="flex flex-col gap-3">
            <div class="h-5 w-36 animate-pulse rounded-lg bg-surface-container-high" />
            <div class="h-12 w-full animate-pulse rounded-full bg-surface-container-high" />
            <div class="h-12 w-full animate-pulse rounded-full bg-surface-container-high" />
          </div>
        </div>
      </div>
    </section>
  )
}

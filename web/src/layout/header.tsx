interface HeaderProps {
  onCreateCandidate?: () => void
}

export function Header({ onCreateCandidate }: HeaderProps) {
  return (
    <header class="fixed top-0 z-50 flex w-full items-center justify-between border-b border-surface-variant/30 bg-background/80 px-8 py-4 shadow-2xl backdrop-blur-xl">
      <h1 class="m-0 text-center text-xl font-black tracking-wider text-primary uppercase md:text-2xl">
        COGNAQUIN
      </h1>
      {onCreateCandidate && (
        <button
          class="flex items-center gap-2 rounded-full bg-primary-container px-5 py-2 text-sm font-bold text-white shadow-lg shadow-primary-container/20 transition-all hover:bg-inverse-primary"
          onClick={onCreateCandidate}
        >
          <span class="material-symbols-outlined text-[20px]">add</span>
          Nuevo Candidato
        </button>
      )}
    </header>
  )
}

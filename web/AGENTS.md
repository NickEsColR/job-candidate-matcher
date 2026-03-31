# Web - AI Agent Ruleset

> **Skills Reference**: For detailed patterns, use these skills:
> - [`pnpm`](../../skills/pnpm/SKILL.md) - Fast Node.js package manager
> - [`preact-ui`](../../skills/preact-ui/SKILL.md) - Preact patterns for UI components
> - [`git-commit`](../../skills/git-commit/SKILL.md) - Conventional commits

### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| Working with Node.js packages (install, run scripts) | `pnpm` |
| Creating or modifying Preact UI components | `preact-ui` |
| Creating a git commit | `git-commit` |

---

## CRITICAL RULES — NON-NEGOTIABLE

### Separation of Concerns (MANDATORY)

> **Components render. Logic computes. Never mix them.**

#### What goes where:

| Location | Contains | Dependencies |
|----------|----------|--------------|
| `cards/` | Card components (display data) | Preact/TSX only |
| `layout/` | Structural components (header, footer, orchestrator) | Preact/TSX only |
| `domain/` | TypeScript interfaces and mock data | NONE (no framework imports) |
| `utils/` | Pure functions (lookup, transform, resolve) | NONE (no framework imports) |
| `app.tsx`, `main.tsx` | Entry point | Preact only |

#### The rule:

- **NEVER** put `find()`, `reduce()`, `filter()`, or any data lookup/transformation inside a `.tsx` component
- **NEVER** import Preact/React in a `.logic.ts` file — these are pure TypeScript
- **ALWAYS** extract business logic to `utils/<entity>.logic.ts` with functions named by domain (`findCandidateById`, not `findSelectedCandidate`)
- **ALWAYS** pass already-resolved data to components via props — components don't fetch, search, or decide what to show
- If a component contains logic to determine WHAT to render, move it to `utils/` and let the component receive the result

#### Forbidden patterns:

```tsx
// ❌ BAD: data lookup inside component
function MyCard({ candidates, selectedId }) {
  const selected = candidates.find(c => c.id === selectedId)
  return <div>{selected.name}</div>
}

// ✅ GOOD: logic extracted, component receives resolved data
import { findCandidateById } from '../utils/candidates.logic'

function MyCard({ candidates, selectedId }) {
  const selected = findCandidateById(candidates, selectedId)
  return <div>{selected.name}</div>
}
```

```
// ❌ BAD: Preact import in logic file
import { useState } from 'preact/hooks'
export function useCandidate() { ... }

// ✅ GOOD: pure TypeScript, zero framework deps
import type { Candidate } from '../domain/types'
export function findCandidateById(candidates: Candidate[], id: string) { ... }
```

---

### Component Naming

- Use short, generic names: `candidate-card.tsx`, not `candidate-profile-card.tsx`
- Name by what it IS (a card), not what it does (profile)
- Avoid feature prefixes: `cards/candidate-card.tsx`, not `cards/evaluations-candidate-card.tsx`

### Types and Data

- ALL interfaces and types live in `domain/types.ts`
- Mock/fixture data lives in `domain/mock-data.ts`
- NEVER create type definitions inside component files

---

## DECISION TREES

### Where does this code go?

```text
Component (renders UI)?          → cards/ or layout/
Pure logic (lookup, transform)?  → utils/<entity>.logic.ts
TypeScript interface/type?       → domain/types.ts
Mock data for development?       → domain/mock-data.ts
Application entry/wiring?        → app.tsx, main.tsx
```

### Adding a new UI component

```text
1. Identify if it's layout (structural) or card (content)
2. Create in layout/ or cards/<name>.tsx
3. If it needs data lookup: create utils/<entity>.logic.ts first
4. Import types from domain/types.ts only
5. Pass data via props — never fetch inside component
```

### Adding a new domain entity

```text
1. Add interfaces to domain/types.ts
2. Add mock data to domain/mock-data.ts (if needed)
3. Create utils/<entity>.logic.ts with pure functions
4. Create card(s) in cards/<name>.tsx consuming utils
```

---

## PROJECT STRUCTURE

```bash
web/
├── src/
│   ├── domain/               # Interfaces, types, mock data
│   ├── layout/               # Structural components (orchestrates the page)
│   ├── cards/                # Content display components
│   ├── utils/                # Pure logic (no framework imports)
│   ├── app.tsx               # Root component
│   ├── main.tsx              # Entry point (render call)
│   └── index.css             # Global styles
├── public/
├── package.json
├── pnpm-lock.yaml
├── tsconfig.json
└── vite.config.ts
```

---

## COMMANDS

```bash
# Development
cd web
pnpm install
pnpm dev

# Build
pnpm build

# Type checking
pnpm exec tsc --noEmit

# Package management
pnpm add <package>
pnpm remove <package>
```

---

## NAMING CONVENTIONS

| Element | Pattern | Example |
|---------|---------|---------|
| Card component | `<entity>-card.tsx` | `candidate-card.tsx` |
| Card export | `<Entity>Card` | `CandidateCard` |
| Layout component | `<name>.tsx` | `dashboard.tsx` |
| Logic file | `<entity>.logic.ts` | `candidates.logic.ts` |
| Logic function | `<verb><Entity>` | `findCandidateById` |
| Type file | `types.ts` | — |
| Mock data | `mock-data.ts` | — |

---

## QA CHECKLIST BEFORE COMMIT

- [ ] `pnpm exec tsc --noEmit` passes
- [ ] No `.tsx` file contains `find()`, `reduce()`, or `filter()` for data lookup
- [ ] No `.logic.ts` file imports from Preact
- [ ] All interfaces are in `domain/types.ts`, not duplicated in components
- [ ] Components receive data via props, not fetching inside
- [ ] New components follow naming convention (`<entity>-card.tsx`)
- [ ] `pnpm build` succeeds

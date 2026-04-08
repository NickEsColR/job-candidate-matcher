---
name: preact-ui
description: >
  Preact UI patterns for building web components with hooks, forms, TypeScript, and composition.
  Trigger: When creating or modifying UI components in web/ using Preact.
license: Apache-2.0
metadata:
  author: NickEsColR
  version: "1.0"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, Context7ResolveLibraryId, Context7QueryDocs
---

## When to Use

- Creating new UI components in `web/src/`
- Building forms and modals in Preact
- Managing local state with Preact hooks
- Typing components and events with TypeScript
- Integrating React-oriented libraries through `preact/compat` when needed

## Critical Patterns

### Pattern 1: Prefer function components + hooks

- Use function components as default.
- Use `useState` for local state and `useEffect` for side effects.
- Keep components small and focused on one responsibility.

### Pattern 2: Use `onInput` for form controls in Preact core

- In Preact core, prefer `onInput` for text input changes.
- `onChange` follows native DOM commit semantics.
- If you need React event behavior for third-party libs, use `preact/compat`.

### Pattern 3: Use controlled inputs only when needed

- Prefer uncontrolled inputs for simple forms.
- Use controlled inputs (`value` + `onInput`) when you need validation, masking, or dynamic UI reactions.

### Pattern 4: Type components and events explicitly in TypeScript

- Type props using interfaces.
- Use `ComponentChildren` for `children`.
- For strict event typing, use `TargetedMouseEvent` and inferred `currentTarget` patterns.

### Pattern 5: Composition first, context second

- Compose with props and children first.
- Introduce Context only for shared cross-tree state.
- Memoize provider values when passing objects/functions to avoid unnecessary updates.

## Code Examples

### Example 1: Basic function component with state

```tsx
import { useState } from 'preact/hooks';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

### Example 2: Modal form with `onInput` (Preact)

```tsx
import { useState } from 'preact/hooks';

interface CandidateFormProps {
  onSubmit: (name: string) => Promise<void>;
  onClose: () => void;
}

export function CandidateFormModal({ onSubmit, onClose }: CandidateFormProps) {
  const [name, setName] = useState('');
  const [saving, setSaving] = useState(false);

  async function handleSubmit(e: Event) {
    e.preventDefault();
    setSaving(true);
    try {
      await onSubmit(name.trim());
      onClose();
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Name
        <input
          value={name}
          onInput={(e) => setName((e.currentTarget as HTMLInputElement).value)}
        />
      </label>
      <button type="submit" disabled={saving || !name.trim()}>
        {saving ? 'Saving...' : 'Save'}
      </button>
      <button type="button" onClick={onClose}>Cancel</button>
    </form>
  );
}
```

### Example 3: Typed component with children

```tsx
import type { ComponentChildren } from 'preact';

interface CardProps {
  title: string;
  children: ComponentChildren;
}

export function Card({ title, children }: CardProps) {
  return (
    <section class="card">
      <h2>{title}</h2>
      <div>{children}</div>
    </section>
  );
}
```

### Example 4: Shared state with Context

```tsx
import { createContext } from 'preact';
import { useContext, useMemo, useState } from 'preact/hooks';

type CounterCtx = { count: number; increment: () => void };
const CounterContext = createContext<CounterCtx | null>(null);

export function CounterProvider({ children }: { children: preact.ComponentChildren }) {
  const [count, setCount] = useState(0);
  const value = useMemo(
    () => ({ count, increment: () => setCount((c) => c + 1) }),
    [count],
  );

  return <CounterContext.Provider value={value}>{children}</CounterContext.Provider>;
}

export function useCounterContext(): CounterCtx {
  const ctx = useContext(CounterContext);
  if (!ctx) throw new Error('useCounterContext must be used inside CounterProvider');
  return ctx;
}
```

## UI Conventions for this Project (`web/`)

- Keep UI in `web/src/`
- Co-locate component + styles when local to one feature
- Use feature folders when screen grows (example: `features/evaluations/components/`)
- Keep API calls in dedicated adapters/helpers (not directly scattered in JSX)
- Model loading/error/empty states explicitly

## Testing Guidance

- Prefer `@testing-library/preact` for component behavior tests.
- Test interactions from user perspective (buttons, input, modal open/close).
- Avoid testing implementation details (state internals).

## Resources

- **Skill**: See [pnpm](../pnpm/SKILL.md) for package management standards.
- **Skill**: See [git-commit](../git-commit/SKILL.md) for commit conventions.

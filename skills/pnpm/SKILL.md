---
name: pnpm
description: >
  Fast, disk space efficient Node.js package manager.
  Trigger: When working with JavaScript/TypeScript packages, Node.js projects, or running frontend build tools.
license: Apache-2.0
metadata:
  author: NickEsColR
  version: "1.0"
---

## When to Use

- Installing Node.js libraries (dependencies)
- Running npm scripts defined in package.json
- Managing frontend dependencies (Preact, Vite, Tailwind, etc.)
- Creating reproducible Node.js environments with pnpm-lock.yaml

## Critical Patterns

1. **Use `pnpm` instead of `npm` or `yarn`** — Faster, uses hard links, deduplicates globally
2. **Always commit `pnpm-lock.yaml`** — Ensures reproducible builds across environments
3. **Use `pnpm add`** instead of `npm install <pkg>` — Adds to package.json + updates lockfile
4. **Use `pnpm run <script>` or `pnpm <script>`** — Both work, shorter form preferred
5. **NEVER use `npm` or `yarn` in this project** — Always pnpm

## Installation

```bash
# Via npm (if migrating)
npm install -g pnpm

# Via corepack (Node.js 16.13+)
corepack enable
corepack prepare pnpm@latest --activate

# Via standalone script
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Windows (PowerShell)
iwr https://get.pnpm.io/install.ps1 -useb | iex
```

Verify: `pnpm --version`

## Package Management

### Add Dependencies

```bash
# Add to dependencies
pnpm add preact

# Add with version constraint
pnpm add "preact@^10.0.0"

# Add dev dependency
pnpm add -D typescript vite

# Add global tool
pnpm add -g pnpm
```

### Remove Dependencies

```bash
pnpm remove lodash
pnpm remove -D jest
```

### Install from Lockfile

```bash
# Install all dependencies from pnpm-lock.yaml
pnpm install

# Frozen lockfile (CI mode — fails if lockfile is outdated)
pnpm install --frozen-lockfile

# Install only production dependencies
pnpm install --prod
```

## Running Scripts

### Pattern: Use `pnpm` instead of `npm run`

```bash
# Run script from package.json
pnpm dev
pnpm build
pnpm test
pnpm lint

# Explicit form (same thing)
pnpm run dev
pnpm run build

# Pass arguments to script
pnpm test -- --watch
pnpm build -- --mode production
```

### Running CLI Tools

```bash
# Run locally installed tool (without global install)
pnpm exec vite
pnpm exec tsc
pnpm exec vitest

# Or use npx equivalent
pnpm dlx create-vite my-app --template preact-ts
```

## Common Patterns by Framework

```bash
# Preact + Vite
pnpm dev              # Dev server
pnpm build            # Production build
pnpm preview          # Preview production build

# Next.js
pnpm dev              # Dev server
pnpm build            # Production build
pnpm start            # Start production server

# Testing
pnpm test             # Run tests
pnpm test:watch       # Watch mode
pnpm test:coverage    # With coverage
```

## Monorepo (if needed later)

```bash
# Workspace commands
pnpm install -w              # Install at workspace root
pnpm add -D typescript -w    # Add to root devDeps
pnpm --filter web dev        # Run script in specific package
pnpm -r build                # Run script in all packages
```

## Quick Reference

| Task | Command |
|------|---------|
| Add dependency | `pnpm add <package>` |
| Add dev dependency | `pnpm add -D <package>` |
| Remove dependency | `pnpm remove <package>` |
| Install from lockfile | `pnpm install --frozen-lockfile` |
| Run script | `pnpm <script>` |
| Run tool | `pnpm exec <tool>` |
| Create project | `pnpm dlx create-<tool>` |
| Update all deps | `pnpm update` |
| Clean cache | `pnpm store prune` |

## Best Practices

- Commit `pnpm-lock.yaml` to version control
- Use `--frozen-lockfile` in CI/CD for consistent builds
- Use `pnpm <script>` shorthand (not `npm run`)
- Use `pnpm exec` for locally installed CLI tools
- NEVER use `npm` or `yarn` in this project — always pnpm
- Use `pnpm add -D` for devDependencies (not `--save-dev`)

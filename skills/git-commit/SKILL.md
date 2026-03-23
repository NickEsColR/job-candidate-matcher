---
name: git-commit
description: >
  Git commit workflow for Job-Candidate-Matcher following conventional commits.
  Trigger: When creating git commits, committing changes, or preparing code for review.
license: Apache-2.0
metadata:
  author: NickEsColR
  version: "1.0"
---

## When to Use

- Creating git commits for any code change
- Committing changes to local branch
- Preparing commits for PR submission
- Analyzing commit history

## Critical Patterns

### Conventional Commits Format
```
<type>(<scope>): <description>
```

| Type | Purpose | Description |
|------|---------|-------------|
| `feat` | New feature | Something added for the user |
| `fix` | Bug fix | Something fixed for the user |
| `docs` | Documentation | Only docs changed |
| `refactor` | Code refactoring | No behavior change |
| `chore` | Maintenance | deps, config, build |
| `test` | Adding/fixing tests | Test files only |
| `ci` | CI/CD changes | GitHub Actions, etc |
| `build` | Build system | Package managers |

**Rules:**
- Description MUST be lowercase
- Description after `:` (colon + space)
- Scope is optional, lowercase

### Branch Naming
Format: `<type>/<description>`

**Examples:**
```
feat/add-candidate-endpoint
fix/validation-error
docs/update-readme
refactor/extract-service
chore/update-deps
```

**Rules:**
- Description MUST be lowercase
- Only `a-z`, `0-9`, `.`, `_`, `-` allowed
- No uppercase, no spaces

## Code Examples

### Valid commit messages
```
feat(candidates): add POST /candidates endpoint
fix(validation): handle empty skills array
docs(readme): update installation instructions
refactor(api): extract candidate service
chore(deps): update fastapi to 0.109
test(candidates): add tests for validation
ci(workflows): add ruff lint check
build(docker): update postgres to 16
```

### Invalid commit messages (will be rejected)
```
Add new feature          ← no type prefix
feat: Add endpoint      ← description should be lowercase
FEAT(api): add endpoint ← type must be lowercase
feat: Add Endpoint      ← description should be lowercase
```

### Stage and commit
```bash
# Stage specific files
git add src/models/candidate.py src/routes/candidates.py

# Stage all changes
git add .

# Commit with conventional format
git commit -m "feat(candidates): add POST /candidates endpoint"

# Amend last commit (only if NOT pushed)
git commit --amend
```

## Commands

```bash
# Check current status
git status

# View staged changes
git diff --cached

# View unstaged changes  
git diff

# Create conventional commit
git commit -m "feat(scope): description"

# View commit history
git log --oneline

# Create branch with naming convention
git checkout -b feat/my-feature

# Unstage files
git reset HEAD <file>

# Discard unstaged changes
git checkout -- <file>
```

## Integration with pr-creation Skill

This skill works with [pr-creation](pr-creation/SKILL.md):

1. Create branch: `git checkout -b feat/my-feature`
2. Make commits: Use conventional commits (this skill)
3. Push: `git push -u origin feat/my-feature`
4. Create PR: Use pr-creation skill

## Resources

- **AGENTS.md**: See [AGENTS.md](../AGENTS.md) for project conventions
- **pr-creation**: See [pr-creation](../skills/pr-creation/SKILL.md) for PR workflow

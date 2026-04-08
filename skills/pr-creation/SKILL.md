---
name: pr-creation
description: >
  Pull request creation workflow for Job-Candidate-Matcher following conventional commits.
  Trigger: When creating a pull request, opening a PR, or preparing changes for review.
license: Apache-2.0
metadata:
  author: NickEsColR
  version: "1.0"
---

## When to Use

- Creating a pull request for any change
- Preparing a branch for submission
- Opening a PR for code review

## Critical Patterns

### Branch Naming
Format: `<type>/<description>`

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat/add-candidate-endpoint` |
| `fix` | Bug fix | `fix/validation-error` |
| `docs` | Documentation | `docs/api-reference` |
| `refactor` | Code refactoring | `refactor/extract-service` |
| `chore` | Maintenance | `chore/update-deps` |

**Rules:**
- Description MUST be lowercase
- Only `a-z`, `0-9`, `.`, `_`, `-` allowed
- No uppercase, no spaces

### Conventional Commits
Format: `<type>(<scope>): <description>`

**Examples:**
```
feat(candidates): add POST /candidates endpoint
fix(validation): handle empty skills array
docs(readme): update installation instructions
```

### PR Checklist

- [ ] Branch follows naming convention
- [ ] Conventional commit format
- [ ] Tests pass locally: `pytest tests/`
- [ ] Lint passes: `ruff check .`
- [ ] Format passes: `ruff format .`
- [ ] No secrets or credentials committed

## Code Examples

### Creating a feature branch
```bash
git checkout -b feat/add-evaluation-endpoint
```

### Conventional commit
```bash
git commit -m "feat(evaluations): add POST /evaluations endpoint"
```

### Push and create PR
```bash
git push -u origin feat/add-evaluation-endpoint
gh pr create --title "feat(evaluations): add POST /evaluations endpoint" --body "Description..."
```

## Commands

```bash
# Create branch
git checkout -b feat/my-feature

# Run checks before PR
pytest tests/
ruff check .
ruff format .

# Push and create PR
git push -u origin feat/my-feature
gh pr create --title "feat(scope): description" --body "Description..."
```

## Resources

- **AGENTS.md**: See [AGENTS.md](../AGENTS.md) for project conventions
- **Testing**: See [AGENTS.md](../AGENTS.md#testing) for test patterns

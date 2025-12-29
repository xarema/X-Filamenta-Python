# Git commit instructions (Conventional Commits)

Use Conventional Commits with optional scope.

Format:
<type>(<scope>): <subject>

Types: feat, fix, refactor, perf, test, docs, chore, build, ci, style

Scopes (use when helpful): backend, frontend, templates, api, auth, deps, ci

Rules:

- Subject in imperative mood, present tense.
- Max ~72 chars for subject.
- No trailing period.
- If needed, add a body with bullet points explaining why + notable behavior changes.
- Mention BREAKING CHANGE: in body when applicable.
  Examples:
- feat(backend): add /health endpoint
- fix(frontend): prevent double submit on htmx forms
- refactor(api): extract validation into service layer

---
applyTo: "**/*.py"
---

Python rules:

- Use `ruff`-compatible style and keep functions small.
- Prefer explicit types and dataclasses for structured data.
- Prefer pure functions for business logic; keep Flask handlers thin.
- Add/adjust pytest tests for any behavior change.

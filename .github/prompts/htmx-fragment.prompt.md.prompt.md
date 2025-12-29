---
mode: "agent"
description: "Create an HTMX endpoint + partial template (Bootstrap 5)"
---

Create a Flask route + Jinja partial for this UI interaction.

User story: ${input:story:Describe the interaction}
Current HTML (if any): ${input:html:Paste existing snippet}

Requirements:

- Return a partial template suitable for hx-target updates.
- Use Bootstrap 5 classes.
- Keep JS minimal; prefer HTMX.
- Include a small pytest test for the route (status + basic behavior).

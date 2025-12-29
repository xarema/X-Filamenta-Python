# GitHub Chat – Windows 11 / PowerShell rules

## Environment

- OS: Windows 11
- Shell: PowerShell (pwsh / Windows PowerShell)
- Python launcher: use `py` (NOT `python`)

## Command rules (mandatory)

- Always write commands for PowerShell.
- Never use `&&` (bash/cmd chaining is not allowed).
- Prefer `;` to chain simple commands in PowerShell.
- If you need conditional chaining, use PowerShell semantics:
  - `if ($?) { <next command> }`
  - or `$LASTEXITCODE` for external commands when needed.

## Python rules

- Always run Python as:
  - `py -m pip ...` (NOT `pip ...`, NOT `python -m pip ...`)
  - `py script.py` or `py -m module`
- If a virtual environment is involved, use PowerShell activation:
  - `.\.venv\Scripts\Activate.ps1`

## Examples

- Install deps:
  - `py -m pip install -r requirements.txt`
- Run app:
  - `py app.py`
- Chain safely (no &&):
  - `py -m pip install -r requirements.txt; if ($?) { py app.py }`

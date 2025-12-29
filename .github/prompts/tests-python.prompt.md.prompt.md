# Copilot Shell Rules (Windows 11 / PowerShell)
**Scope:** All terminal commands must be compatible with **Windows 11 PowerShell**.
**Do not assume:** bash, zsh, WSL, Git Bash, MSYS2, Cygwin.

## 1) Mandatory environment
- Shell: **PowerShell** (Windows 11)
- Path separator: `\` (Windows paths)
- Chain commands with `;` or new lines (NOT `&&`)
- Use PowerShell pipeline objects and cmdlets.

## 2) Absolute prohibitions (Linux-only commands)
Never suggest or use:
- `head`, `tail`, `grep`, `sed`, `awk`, `cut`, `tr`, `xargs`
- `ls` (prefer PowerShell cmdlet forms), `cat`, `rm`, `cp`, `mv`, `touch` (use PowerShell equivalents)
- `find` (use `Get-ChildItem -Recurse`)
- `export`, `which`, `chmod`, `chown`
- `curl | bash` style commands

If the user pasted such commands, convert them to PowerShell equivalents.

## 3) Standard equivalents (use these)
### Files / folders
- List directory: `Get-ChildItem`  (alias: `gci`)
- Current directory: `Get-Location`
- Change directory: `Set-Location <path>`  (alias: `cd`)
- Create folder: `New-Item -ItemType Directory -Path <path>`
- Create file: `New-Item -ItemType File -Path <file>`
- Copy: `Copy-Item <src> <dst> -Recurse -Force`
- Move/Rename: `Move-Item <src> <dst> -Force` or `Rename-Item <path> -NewName <name>`
- Remove: `Remove-Item <path> -Recurse -Force`
- Check existence: `Test-Path <path>`

### Text output / filtering (replacement for grep/head/tail)
- Read file: `Get-Content <file>`
- First N lines (head): `Get-Content <file> | Select-Object -First 20`
- Last N lines (tail):  `Get-Content <file> | Select-Object -Last 40`
- Follow file (tail -f): `Get-Content <file> -Tail 40 -Wait`
- Search text (grep): `Select-String -Pattern "<regex>" <file>`
- Search from pipeline:
  `someCommand 2>&1 | Select-String -Pattern "ERROR|WARN|OK"`
- Print only matched lines:
  `... | Select-String -Pattern "..." | ForEach-Object { $_.Line }`

### Processes
- List processes: `Get-Process`
- Kill process: `Stop-Process -Id <pid> -Force`

### Networking
- HTTP request (replacement for wget/curl usage): `Invoke-WebRequest <url> -OutFile <file>`
- REST JSON: `Invoke-RestMethod <url>`

### Archives
- Zip folder: `Compress-Archive -Path <path> -DestinationPath <zipfile> -Force`
- Unzip: `Expand-Archive -Path <zipfile> -DestinationPath <folder> -Force`

### JSON / objects
- Convert JSON -> object: `Get-Content <file> | ConvertFrom-Json`
- Convert object -> JSON: `<obj> | ConvertTo-Json -Depth 10`

## 4) PowerShell-specific rules
- Use `$env:VAR = "value"` to set env vars for current session.
- Use `Write-Host` only for UX; prefer returning objects/strings.
- Always capture errors when debugging: append `2>&1` and pipe to `Select-String` if needed.
- Prefer double quotes for string interpolation, single quotes for literals.
- Avoid backtick line continuations unless necessary; prefer parentheses or splatting.

## 5) Python execution (Windows venv-friendly)
- Prefer the repo venv interpreter when present:
  - `.\.venv\Scripts\python.exe <script.py>`
- Or run modules:
  - `.\.venv\Scripts\python.exe -m pytest`
- If you must use the launcher:
  - `py -m pip install -r requirements.txt`
  - `py -m pytest`
- Never assume `python` exists on PATH unless explicitly confirmed.

## 6) Command formatting guidelines (Copilot output)
- Provide commands as **PowerShell** blocks, one per line, or chained with `;`.
- Always use Windows paths (e.g., `D:\xarema\...`) and quote paths with spaces.
- If admin is required, explicitly say so and provide:
  `Start-Process PowerShell -Verb RunAs`

## 7) Example conversions
- Linux:
  `python test.py 2>&1 | head -20`
  PowerShell:
  `.\.venv\Scripts\python.exe test.py 2>&1 | Select-Object -First 20`

- Linux:
  `... | tail -40`
  PowerShell:
  `... | Select-Object -Last 40`

- Linux:
  `... | grep -E "TEST|OK|ERROR"`
  PowerShell:
  `... | Select-String -Pattern "TEST|OK|ERROR"`

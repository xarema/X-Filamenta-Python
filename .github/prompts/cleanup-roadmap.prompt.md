---
mode: "agent"
description: "Clean and organize . roadmap/ directory by archiving completed phases, removing obsolete files, and validating structure"
---

# Cleanup Roadmap Directory

**Task:** Clean, organize, and validate the `.roadmap/` directory structure by archiving completed phases, removing obsolete files, reorganizing content, and ensuring consistency.

---

## Input Required

### Cleanup Scope
${input: scope: What to clean? (all|completed-phases|old-reports|structure-only)}

### Archive Completed Phases
${input:archive: Archive completed phases to /archive?  (yes|no)}

### Remove Old Reports
${input:remove_reports:Remove analysis reports older than X days? (30|60|90|never)}

### Reorganize Structure
${input:reorganize:Reorganize directory structure?  (yes|no)}

### Validate Links
${input:validate: Validate all Markdown links? (yes|no)}

---

## MANDATORY:   Pre-Cleanup Process

### 1. Prerequisites Check

**CRITICAL:  This prompt should be run AFTER update-roadmap**

- [ ] `update-roadmap` has been executed recently
- [ ] Latest status report exists in `Analysis_reports/`
- [ ] Roadmap content is up-to-date
- [ ] You understand what will be archived/deleted

**⚠️ WARNING:**
- This prompt will MOVE and DELETE files
- Create backup before running:  `Copy-Item . roadmap . roadmap.backup -Recurse`

### 2. Read Current Structure

**Analyze:**
- [ ] `.roadmap/README.md` — Identify completed phases
- [ ] `.roadmap/PHASES/` — Count active vs.  completed phases
- [ ] `.roadmap/archive/` — Check existing archives
- [ ] `Analysis_reports/` — Count old reports

### 3. Identify Cleanup Targets

**Files to potentially remove:**
- Backup files (`.bak`, `~`, `.tmp`)
- Old analysis reports (>90 days)
- Empty directories
- Orphaned files (not referenced anywhere)

**Phases to potentially archive:**
- Phases marked 100% complete
- Phases older than X months and completed

---

## Cleanup Workflow

### Step 1: Backup Current State

**Create backup:**

```powershell
# Windows PowerShell
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item . roadmap ". roadmap.backup-$timestamp" -Recurse
Write-Host "✅ Backup created: .roadmap.backup-$timestamp"
```

```bash
# Linux/Mac
timestamp=$(date +%Y%m%d-%H%M%S)
cp -r .roadmap ". roadmap.backup-$timestamp"
echo "✅ Backup created: .roadmap.backup-$timestamp"
```

---

### Step 2: Remove Obsolete Files

**Targets:**

#### A.  Backup and Temporary Files

```
Files to remove:
- *.bak
- *~
- *.tmp
- *.swp
- . DS_Store
- Thumbs.db
```

**Action:**
```powershell
# Remove backup files
Get-ChildItem -Path . roadmap -Recurse -Include *.bak,*~,*. tmp,*.swp,. DS_Store,Thumbs.db | Remove-Item -Force
```

#### B. Old Analysis Reports

**Criteria:**
- Reports older than X days (default: 90)
- Keep latest 10 reports regardless of age
- Keep milestone reports (tagged with "milestone" in filename)

**Action:**
```powershell
# List old reports (>90 days)
$cutoffDate = (Get-Date).AddDays(-90)
$oldReports = Get-ChildItem -Path Analysis_reports -Filter "*roadmap*. md" | 
    Where-Object { $_.LastWriteTime -lt $cutoffDate -and $_.Name -notmatch "milestone" } |
    Sort-Object LastWriteTime |
    Select-Object -SkipLast 10

# Review before deletion
$oldReports | Format-Table Name, LastWriteTime

# Delete (if confirmed)
# $oldReports | Remove-Item -Force
```

#### C. Empty Directories

**Action:**
```powershell
# Find and remove empty directories
Get-ChildItem -Path .roadmap -Recurse -Directory | 
    Where-Object { (Get-ChildItem $_.FullName -Force | Measure-Object).Count -eq 0 } |
    Remove-Item -Force
```

---

### Step 3: Archive Completed Phases

**Identify completed phases:**

From latest `update-roadmap` report, identify phases at 100% completion.

**Example:**
- Phase 1: Infrastructure Setup — ✅ 100% (Completed 2025-01-15)
- Phase 2: Backend Routes — 🔄 65% (In Progress)

**Archive structure:**

```
.roadmap/
├── archive/
│   ├── PHASE_1_Infrastructure_Setup.md        ← Archived
│   ├── PHASE_1_completion_report.md           ← Summary
│   └── 2025-01-15_Phase1_archive. md           ← Archive log
├── PHASES/
│   ├── PHASE_2. md                             ← Active
│   ├── PHASE_3.md                             ← Active
│   └── PHASE_4.md                             ← Active
```

**Archive process:**

1. **Create archive directory (if not exists):**
   ```powershell
   New-Item -Path .roadmap/archive -ItemType Directory -Force
   ```

2. **Move completed phase:**
   ```powershell
   Move-Item . roadmap/PHASES/PHASE_1. md .roadmap/archive/PHASE_1_Infrastructure_Setup.md
   ```

3. **Create completion report:**

```markdown
# Phase 1 Completion Report

**Phase:** Phase 1 — Infrastructure Setup  
**Status:** ✅ Completed  
**Completion Date:** 2025-01-15  
**Duration:** 15 days (2025-01-01 to 2025-01-15)  
**Archived:** 2025-01-20

---

## Final Status

**Total Features:** 15  
**Completed:** 15 (100%)  
**Test Coverage:** 95%  
**Documentation:** Complete

---

## Key Achievements

- ✅ Flask application structure created
- ✅ Database models implemented
- ✅ Authentication system complete
- ✅ Basic admin panel functional
- ✅ All tests passing

---

## Implementation Evidence

**Files Created:**
- backend/src/models/user.py
- backend/src/routes/auth.py
- backend/src/services/auth_service.py
- tests/test_auth.py (30 tests, 100% pass)

**Documentation:**
- docs/architecture/database.md
- docs/features/authentication.md

---

## Lessons Learned

1. [Lesson 1]
2. [Lesson 2]

---

## Archived Location

Original file:  `.roadmap/PHASES/PHASE_1.md`  
Archive file: `.roadmap/archive/PHASE_1_Infrastructure_Setup. md`  
Archive date: 2025-01-20
```

4. **Create archive log:**

```markdown
# Archive Log:  2025-01-20

**Archived by:** Cleanup Roadmap Agent  
**Reason:** Phase 1 completed (100%)

---

## Archived Items

- PHASE_1.md → archive/PHASE_1_Infrastructure_Setup.md
- Phase 1 completion report created

---

## Remaining Active Phases

- Phase 2: Backend Routes (65%)
- Phase 3: Testing (0%)
- Phase 4: Business Features (0%)
```

---

### Step 4: Reorganize Structure (Optional)

**Recommended structure:**

```
.roadmap/
├── README.md                    ← Main overview
├── PROGRESS.md                  ← Metrics & velocity
├── TIMELINE.md                  ← Milestones
├── INDEX.md                     ← Quick navigation (NEW)
├── PHASES/
│   ├── PHASE_2.md              ← Active phases only
│   ├── PHASE_3.md
│   └── PHASE_4.md
├── archive/
│   ├── completed/              ← Completed phases (NEW)
│   │   ├── PHASE_1_Infrastructure_Setup.md
│   │   └── PHASE_1_completion_report.md
│   ├── deprecated/             ← Deprecated/cancelled (NEW)
│   └── logs/                   ← Archive logs (NEW)
│       └── 2025-01-20_archive.md
└── reports/                    ← Analysis reports shortcut (NEW)
    → ../Analysis_reports/      (symbolic link)
```

**Create new directories:**

```powershell
# Create structure
New-Item -Path .roadmap/archive/completed -ItemType Directory -Force
New-Item -Path .roadmap/archive/deprecated -ItemType Directory -Force
New-Item -Path .roadmap/archive/logs -ItemType Directory -Force

# Create symbolic link to reports
New-Item -ItemType SymbolicLink -Path .roadmap/reports -Target ../Analysis_reports
```

---

### Step 5: Validate Structure

#### A. Validate Markdown Links

**Check all links in roadmap files:**

```powershell
# PowerShell script to validate links
$files = Get-ChildItem -Path .roadmap -Recurse -Filter *.md

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Extract Markdown links [text](path)
    $links = [regex]::Matches($content, '\[([^\]]+)\]\(([^)]+)\)')
    
    foreach ($link in $links) {
        $linkPath = $link.Groups[2].Value
        
        # Skip URLs (http/https)
        if ($linkPath -match '^https?://') { continue }
        
        # Check if file exists
        $fullPath = Join-Path (Split-Path $file.FullName) $linkPath
        if (-not (Test-Path $fullPath)) {
            Write-Host "❌ Broken link in $($file.Name): $linkPath" -ForegroundColor Red
        }
    }
}
```

**Action:**
- Fix broken links
- Update references to archived files
- Remove links to deleted files

#### B. Validate Consistency

**Check:**
- [ ] Phase numbers sequential (PHASE_2, PHASE_3, PHASE_4)
- [ ] No gaps in numbering
- [ ] All phases referenced in README. md
- [ ] Progress percentages match feature counts
- [ ] Dates consistent across files

#### C. Validate Naming Conventions

**Standard:**
- Phase files: `PHASE_X.md` (uppercase, underscore)
- Archive files: `PHASE_X_Name.md`
- Reports: `YYYY-MM-DD_HH-mm_topic.md`

**Rename if needed:**

```powershell
# Example:  Rename inconsistent files
Rename-Item .roadmap/PHASES/phase2.md PHASE_2.md
Rename-Item .roadmap/PHASES/Phase-3.md PHASE_3.md
```

---

### Step 6: Generate Index File

**Create:** `.roadmap/INDEX.md`

```markdown
# Roadmap Index

**Last Updated:** YYYY-MM-DD  
**Quick Navigation**

---

## 📊 Overview

- [Main Roadmap](README.md)
- [Progress Tracking](PROGRESS.md)
- [Timeline & Milestones](TIMELINE.md)

---

## 🚀 Active Phases

| Phase | Name | Status | File |
|-------|------|--------|------|
| 2 | Backend Routes & Templates | 🔄 65% | [PHASE_2.md](PHASES/PHASE_2.md) |
| 3 | Testing & Validation | ⏸️ 0% | [PHASE_3.md](PHASES/PHASE_3.md) |
| 4 | Business Features | ⏸️ 0% | [PHASE_4.md](PHASES/PHASE_4.md) |

---

## ✅ Completed Phases (Archived)

| Phase | Name | Completed | Archive |
|-------|------|-----------|---------|
| 1 | Infrastructure Setup | 2025-01-15 | [PHASE_1](archive/completed/PHASE_1_Infrastructure_Setup.md) |

---

## 📝 Recent Reports

- [2025-01-20 Roadmap Status](../Analysis_reports/2025-01-20_roadmap-status. md)
- [2025-01-13 Roadmap Status](../Analysis_reports/2025-01-13_roadmap-status.md)
- [2025-01-06 Roadmap Status](../Analysis_reports/2025-01-06_roadmap-status.md)

---

## 🗂️ Archive

- [Completed Phases](archive/completed/)
- [Deprecated Features](archive/deprecated/)
- [Archive Logs](archive/logs/)

---

**Navigation Tips:**
- Click phase links to see detailed progress
- Check reports for latest analysis
- Review archive for completed work history
```

---

### Step 7: Update README.md

**Update `.roadmap/README.md`:**

Add reference to cleanup and index:

```markdown
## 📁 Directory Structure

```
.roadmap/
├── README.md           ← This file (overview)
├── INDEX.md            ← Quick navigation
├── PROGRESS.md         ← Metrics & velocity
├── TIMELINE.md         ← Milestones
├── PHASES/             ← Active phases (in progress or planned)
├── archive/            ← Completed and deprecated phases
└── reports/            → Analysis reports (link to ../Analysis_reports/)
```

## 🧹 Maintenance

**Last Cleanup:** YYYY-MM-DD  
**Next Scheduled Cleanup:** YYYY-MM-DD (monthly)

For cleanup procedures, see [. github/prompts/cleanup-roadmap.prompt.md]
```

---

## Cleanup Report

**Generate:** `Analysis_reports/YYYY-MM-DD_HH-mm_roadmap-cleanup.md`

```markdown
# Roadmap Cleanup Report

**Date:** YYYY-MM-DD  
**Scope:** [all | completed-phases | old-reports]  
**Executed by:** Cleanup Roadmap Agent

---

## Summary

- **Files Removed:** X
- **Phases Archived:** Y
- **Reports Removed:** Z
- **Directories Cleaned:** W
- **Links Fixed:** V

---

## Actions Taken

### Files Removed

**Backup/Temp Files:**
- . roadmap/PHASES/PHASE_1.md. bak
- .roadmap/. DS_Store
- .roadmap/README.md~

**Total:** 3 files

---

### Phases Archived

**Moved to archive/completed/:**
- PHASE_1.md → PHASE_1_Infrastructure_Setup. md (Completed 2025-01-15)

**Completion reports created:**
- archive/completed/PHASE_1_completion_report.md

**Total:** 1 phase archived

---

### Old Reports Removed

**Criteria:** Reports older than 90 days (kept latest 10)

**Removed:**
- Analysis_reports/2024-10-15_roadmap-status. md (107 days old)
- Analysis_reports/2024-10-22_roadmap-status.md (100 days old)

**Kept:**
- All reports from last 90 days
- 10 most recent reports regardless of age

**Total:** 2 reports removed

---

### Directories Cleaned

**Empty directories removed:**
- .roadmap/old/
- .roadmap/PHASES/archive/

**Total:** 2 directories

---

### Links Validated

**Broken links fixed:**
- README.md: Updated link to archived PHASE_1.md
- PROGRESS.md: Fixed reference to removed report

**Total:** 2 links fixed

---

### Structure Changes

**New directories created:**
- .roadmap/archive/completed/
- .roadmap/archive/deprecated/
- .roadmap/archive/logs/

**New files created:**
- . roadmap/INDEX.md
- .roadmap/archive/logs/2025-01-20_archive.md

---

## Before/After

### Before Cleanup

```
.roadmap/ (45 files, 12 MB)
├── README.md
├── PHASES/ (5 files)
│   ├── PHASE_1.md (completed, should be archived)
│   ├── PHASE_1. md.bak (backup)
│   ├── PHASE_2.md
│   ├── PHASE_3.md
│   └── PHASE_4.md
├── archive/ (empty)
└── . DS_Store
```

### After Cleanup

```
.roadmap/ (38 files, 10 MB)
├── README.md
├── INDEX.md (NEW)
├── PROGRESS.md
├── TIMELINE.md
├── PHASES/ (3 files)
│   ├── PHASE_2.md
│   ├── PHASE_3.md
│   └── PHASE_4.md
├── archive/
│   ├── completed/
│   │   ├── PHASE_1_Infrastructure_Setup.md
│   │   └── PHASE_1_completion_report.md
│   ├── deprecated/ (empty, ready for use)
│   └── logs/
│       └── 2025-01-20_archive.md
└── reports/ → ../Analysis_reports/ (symlink)
```

**Space saved:** 2 MB  
**Files removed:** 7  
**Structure improved:** ✅

---

## Validation Results

### Link Validation
- ✅ All Markdown links valid
- ✅ No broken references
- ✅ Archive links updated

### Naming Consistency
- ✅ All phase files follow PHASE_X. md convention
- ✅ Archive files properly named
- ✅ Report filenames consistent

### Structure Validation
- ✅ No empty directories (except new archive subdirs)
- ✅ Sequential phase numbering
- ✅ README.md references all active phases

---

## Recommendations

1. **Schedule regular cleanup:**
   - Monthly cleanup (first Monday of month)
   - After each phase completion
   - Quarterly full audit

2. **Backup strategy:**
   - Keep cleanup backups for 30 days
   - Store in `.roadmap. backups/` (not in git)

3. **Archive policy:**
   - Archive phases at 100% completion
   - Keep last 90 days of reports
   - Document reasons for deprecation

---

## Next Cleanup

**Scheduled:** YYYY-MM-DD (in 30 days)  
**Trigger:** Monthly schedule OR Phase 2 completion
```

---

## Validation Checklist

Before finalizing cleanup:

### Safety
- [ ] Backup created successfully
- [ ] Backup location documented
- [ ] No critical files deleted
- [ ] Archive process reversible

### Completeness
- [ ] All obsolete files removed
- [ ] All completed phases archived
- [ ] All empty directories removed
- [ ] All broken links fixed

### Structure
- [ ] Directory structure follows standard
- [ ] INDEX.md created and accurate
- [ ] README.md updated
- [ ] Archive properly organized

### Validation
- [ ] All Markdown links valid
- [ ] Naming conventions consistent
- [ ] References updated (README, PROGRESS, etc.)
- [ ] Cleanup report generated

### Communication
- [ ] Team notified of cleanup
- [ ] Archive locations documented
- [ ] Next cleanup scheduled

---

## Rollback Procedure

**If cleanup went wrong:**

```powershell
# 1. Find backup
Get-ChildItem -Filter ".roadmap.backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# 2. Restore backup
$latestBackup = (Get-ChildItem -Filter ". roadmap.backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1).Name
Remove-Item . roadmap -Recurse -Force
Copy-Item $latestBackup .roadmap -Recurse
Write-Host "✅ Restored from backup:  $latestBackup"

# 3. Document rollback
# Create Analysis_reports/YYYY-MM-DD_cleanup-rollback.md
```

---

## Files Created/Modified

```
.roadmap/INDEX.md                                    ← Navigation file (NEW)
.roadmap/README.md                                   ← Updated structure section
.roadmap/archive/completed/                          ← Archived phases (NEW)
.roadmap/archive/deprecated/                         ← Deprecated features (NEW)
.roadmap/archive/logs/                               ← Archive logs (NEW)
.roadmap/reports/                                    ← Symlink to reports (NEW)
Analysis_reports/YYYY-MM-DD_HH-mm_roadmap-cleanup.md ← Cleanup report (NEW)
.roadmap. backup-YYYYMMDD-HHMMSS/                     ← Backup (excluded from git)
```

---

## Don'ts

- ❌ Run cleanup WITHOUT running update-roadmap first
- ❌ Delete files without backup
- ❌ Archive phases that are not 100% complete
- ❌ Remove reports without checking retention policy
- ❌ Skip link validation
- ❌ Forget to update README.md and INDEX.md
- ❌ Delete files manually (use the prompt process)
- ❌ Skip cleanup report generation

---

## References

- `.github/prompts/update-roadmap.prompt.md` — Update roadmap (run BEFORE cleanup)
- `.github/prompts/ROADMAP_WORKFLOW.md` — Workflow guide
- `.roadmap/README.md` — Main roadmap
- `.github/copilot-instructions.md` — General rules

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.   All rights reserved.  

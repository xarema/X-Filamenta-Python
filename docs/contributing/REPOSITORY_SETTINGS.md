# Repository Configuration Recommendations

This document provides recommended GitHub repository settings for X-Filamenta-Python.

## 📌 Repository Topics

**Recommended topics to add on GitHub:**

```
flask
python
htmx
bootstrap
web-application
2fa-authentication
admin-panel
internationalization
redis-cache
sqlite
mysql
postgresql
cpanel
docker
agpl-3-0
python312
rest-api
responsive-web
security
open-source
```

**How to add topics:**
1. Go to repository homepage on GitHub
2. Click ⚙️ gear icon next to "About"
3. Add topics from the list above
4. Save changes

**Benefits:**
- Improved discoverability
- Better GitHub search results
- Relevant recommendations to users
- Technology stack visibility

---

## 🛡️ Branch Protection Rules

### Main Branch Protection

**Recommended settings for `main` branch:**

#### General
- ✅ **Require a pull request before merging**
  - Required approvals: 1
  - Dismiss stale approvals when new commits are pushed
  - Require review from Code Owners

#### Status Checks
- ✅ **Require status checks to pass before merging**
  - Required checks:
    - `CI / test` (from ci.yml)
    - `🧹 Lint / lint-python` (from lint.yml)
    - `🧹 Lint / lint-javascript` (from lint.yml)
    - `🔒 Security Scan / dependency-scan` (from security.yml)

#### Additional Settings
- ✅ **Require conversation resolution before merging**
- ✅ **Require linear history** (enforce fast-forward or squash merge)
- ✅ **Do not allow bypassing the above settings**
- ❌ **Allow force pushes** (disabled)
- ❌ **Allow deletions** (disabled)

### Develop Branch Protection

**Recommended settings for `develop` branch:**

#### General
- ✅ **Require a pull request before merging**
  - Required approvals: 1
  - Allow specified actors to bypass (repository admins only)

#### Status Checks
- ✅ **Require status checks to pass before merging**
  - Required checks:
    - `CI / test`
    - `🧹 Lint / lint-python`

#### Additional Settings
- ✅ **Require conversation resolution before merging**
- ✅ **Allow force pushes** (enabled for feature branch rebasing)
- ❌ **Allow deletions** (disabled)

---

## 🔀 Merge Strategies

**Recommended merge methods:**

### Main Branch
- ✅ **Squash and merge** (preferred)
- ✅ **Rebase and merge** (allowed)
- ❌ **Merge commits** (disabled for cleaner history)

**Rationale:**
- Squash keeps main history linear and clean
- Each PR becomes a single commit
- Easier to revert features
- Better changelog generation

### Develop Branch
- ✅ **Squash and merge** (preferred)
- ✅ **Rebase and merge** (allowed)
- ✅ **Merge commits** (allowed for integration)

**Rationale:**
- More flexibility for development
- Integration commits preserve branch history
- Easier collaboration on feature branches

---

## 🔔 Notifications & Automation

### Dependabot
Already configured (`.github/dependabot.yml`):
- ✅ Weekly Python dependency updates
- ✅ Weekly npm dependency updates
- ✅ Weekly GitHub Actions updates

### Code Scanning
Already configured (`.github/workflows/security.yml`):
- ✅ CodeQL analysis (Python, JavaScript)
- ✅ Secret scanning (TruffleHog)
- ✅ Dependency vulnerability scanning
- ✅ Weekly scheduled scans

### Code Owners
Already configured (`.github/CODEOWNERS`):
- Automatic review requests
- Ensures critical files reviewed by maintainers

---

## 📋 How to Apply These Settings

### Via GitHub Web UI

1. **Branch Protection:**
   - Go to: Settings → Branches → Add rule
   - Enter branch name pattern: `main` or `develop`
   - Check recommended options above
   - Click "Create" or "Save changes"

2. **Merge Methods:**
   - Go to: Settings → General → Pull Requests
   - Select allowed merge methods
   - Click "Save"

3. **Topics:**
   - Go to: Repository homepage
   - Click ⚙️ next to "About"
   - Add topics
   - Click "Save"

### Via GitHub API (Optional)

```bash
# Set branch protection (requires admin access)
gh api repos/xarema/X-Filamenta-Python/branches/main/protection \
  --method PUT \
  --input branch-protection.json

# Add topics
gh api repos/xarema/X-Filamenta-Python/topics \
  --method PUT \
  --field names='["flask","python","htmx","bootstrap","web-application"]'
```

---

## ✅ Verification Checklist

After applying settings, verify:

- [ ] Main branch cannot be pushed to directly
- [ ] PRs require at least 1 approval
- [ ] CI checks must pass before merge
- [ ] Force pushes blocked on main
- [ ] Topics visible on repository homepage
- [ ] Dependabot creating PRs weekly
- [ ] Security scans running on schedule

---

## 📚 References

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Merge Strategies](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges)
- [Repository Topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)

---

**Note:** These are recommendations based on best practices. Adjust based on team size and workflow preferences.

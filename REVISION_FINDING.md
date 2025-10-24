# Revision History Finding

## Request
Find the revision when line 25 of `go-checks.yml` was introduced.

## Finding

**File:** `.github/workflows/go-checks.yml`  
**Line 25:** `lint-target:`

### Commit Details
- **Commit Hash:** `51aa41c0f700c8c8b7b0d2a5566d5130f15294d0`
- **Author:** Olatunde Alex-Oni <tunde.alexoni@yahoo.com>
- **Date:** Tuesday, October 21, 2025 at 12:26:28 +0100
- **Pull Request:** #131
- **PR Title:** "update logic to get secret for tailscale from 1password"

### Context
This commit was a merge commit that initially created the `go-checks.yml` workflow file. The commit is marked as "grafted", indicating it represents the root of the repository's history.

Line 25 defines the `lint-target` input parameter for the workflow, which:
- Type: `string`
- Required: `false`
- Default: `"lint"`
- Description: "Lint Make target"

### Investigation Method
The finding was determined using:
```bash
git blame -L 25,25 .github/workflows/go-checks.yml
git log -L 25,25:.github/workflows/go-checks.yml
```

# GitHub Actions Workflows

## Reusable Workflows

A list of available reusable workflows can be found in the
[`.github/workflows` directory](https://github.com/remerge/workflows/tree/main/.github/workflows).

Each workflow defines its own `inputs`, which you can use to understand how to call it from your repository.

### Example Usage

To use one of these workflows, reference it in your repository's workflow file:

```yaml
name: Example CI

on:
  push:
    branches: [main]

jobs:
  ci:
    uses: remerge/workflows/.github/workflows/ci.yml@main
    with:
      node-version: 20
      run-tests: true
```

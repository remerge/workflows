#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./compute_hash.sh \
#     "europe-west4-docker.pkg.dev/artifact-registry-ff9b/github-actions/default" \
#     "k8s,docs,**/*.md"

IMAGE=${1:-""}
EXCLUDES=${2:-""}

# Enable extended globbing and recursive globs (**)
shopt -s globstar extglob nullglob

# Build find command dynamically
FIND_CMD=(find . -type f)

IFS=',' read -ra PATTERNS <<<"$EXCLUDES"
for pattern in "${PATTERNS[@]}"; do
    # Trim whitespace
    pattern=$(echo "$pattern" | xargs)
    [[ -n $pattern ]] && FIND_CMD+=(! -path "./$pattern")
done

# Compute deterministic content-based hash
TAG=$("${FIND_CMD[@]}" -exec sha256sum {} \; | sort | sha256sum | cut -d' ' -f1)

# Check if image exists in registry
if docker manifest inspect "$IMAGE:$TAG" >/dev/null 2>&1; then
    echo "✅ Image $IMAGE:$TAG already exists - skipping build"
    EXISTS="true"
else
    echo "🚀 Image $IMAGE:$TAG not found — proceed to build"
    EXISTS="false"
fi

# Export values for GitHub Actions (if running inside a workflow)
if [[ -n ${GITHUB_OUTPUT:-} ]]; then
    echo "image=$IMAGE:$TAG" >>"$GITHUB_OUTPUT"
    echo "exists=$EXISTS" >>"$GITHUB_OUTPUT"
fi

# Also print for local debugging
echo "image=$IMAGE:$TAG"
echo "EXISTS=$EXISTS"

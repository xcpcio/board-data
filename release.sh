#!/usr/bin/env bash

set -euo pipefail

readonly tag="${1:-$(date '+v%Y.%m.%d.%H%M')}"
readonly tag_pattern='^v[0-9]{4}\.[0-9]{2}\.[0-9]{2}\.[0-9]{4}$'

if [[ ! "${tag}" =~ ${tag_pattern} ]]; then
  echo "Invalid tag: ${tag}" >&2
  echo "Expected format: vYYYY.MM.DD.HHMM, for example v2026.06.17.0935" >&2
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree is not clean. Commit or stash changes before releasing." >&2
  exit 1
fi

if git rev-parse --verify --quiet "refs/tags/${tag}" >/dev/null; then
  echo "Tag already exists: ${tag}" >&2
  exit 1
fi

echo "Creating release tag: ${tag}"
git tag -a "${tag}" -m "Release ${tag}"

echo "Pushing release tag: ${tag}"
git push origin "${tag}"

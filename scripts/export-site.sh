#!/usr/bin/env bash
set -euo pipefail

SITE_DIR="${SITE_DIR:-/site}"

if [[ -z "${EXPORT_DATA_DIR:-}" ]]; then
  echo "Error: EXPORT_DATA_DIR is not set" >&2
  exit 1
fi

if [[ ! -d "$SITE_DIR" ]]; then
  echo "Error: site directory does not exist: $SITE_DIR" >&2
  exit 1
fi

mkdir -p "$EXPORT_DATA_DIR"
cp -a "$SITE_DIR/." "$EXPORT_DATA_DIR/"

echo "Copied $SITE_DIR to $EXPORT_DATA_DIR"

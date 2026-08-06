#!/usr/bin/env bash
set -euo pipefail

readonly ZERO_SHA="0000000000000000000000000000000000000000"
readonly TARGETS="config.json run.json team.json seat_map.json organizations.json"
readonly DATA_DIR="${DATA_DIR:-data}"
readonly VALIDATE_SCRIPT="${VALIDATE_SCRIPT:-./python/validate_data.py}"
readonly POST_COMMENTS_SCRIPT="${POST_COMMENTS_SCRIPT:-./python/post_validate_pr_comments.py}"
readonly REPORT_JSON="${REPORT_JSON:-./validate-report.json}"

BASE="${1:-}"
COMMIT_SHA="${2:-${GITHUB_SHA:-}}"

post_pr_comments_if_needed() {
  if [[ "${GITHUB_EVENT_NAME:-}" != "pull_request" ]]; then
    return 0
  fi
  if [[ ! -f "${REPORT_JSON}" ]]; then
    return 0
  fi

  local args=("${REPORT_JSON}")
  if [[ -n "${COMMIT_SHA}" ]]; then
    args+=(--commit "${COMMIT_SHA}")
  fi
  uv run "${POST_COMMENTS_SCRIPT}" "${args[@]}"
}

validate_dirs() {
  local status=0
  uv run "${VALIDATE_SCRIPT}" --report-json "${REPORT_JSON}" "$@" || status=$?
  post_pr_comments_if_needed || true
  return "${status}"
}

if [[ -z "${BASE}" || "${BASE}" == "${ZERO_SHA}" ]]; then
  echo "No valid base commit; validating all data."
  validate_dirs "./${DATA_DIR}"
  exit $?
fi

changed_files=()
while IFS= read -r file; do
  [[ -n "${file}" ]] && changed_files+=("${file}")
done < <(git diff --name-only --diff-filter=ACMR "${BASE}"...HEAD -- "${DATA_DIR}/" || true)

if [[ "${#changed_files[@]}" -eq 0 ]]; then
  echo "No changed files under ./${DATA_DIR}; skip validate."
  exit 0
fi

echo "Changed files under ./${DATA_DIR}:"
printf '  %s\n' "${changed_files[@]}"

contest_dirs_file="$(mktemp)"
trap 'rm -f "${contest_dirs_file}"' EXIT

for file in "${changed_files[@]}"; do
  dir=$(dirname "${file}")
  while [[ "${dir}" != "." && "${dir}" != "${DATA_DIR}" ]]; do
    found=0
    for target in ${TARGETS}; do
      if [[ -f "${dir}/${target}" ]]; then
        echo "${dir}" >>"${contest_dirs_file}"
        found=1
        break
      fi
    done
    if [[ "${found}" -eq 1 ]]; then
      break
    fi
    dir=$(dirname "${dir}")
  done
done

if [[ ! -s "${contest_dirs_file}" ]]; then
  echo "No contest dirs to validate; skip."
  exit 0
fi

dirs=()
while IFS= read -r dir; do
  [[ -n "${dir}" ]] && dirs+=("${dir}")
done < <(sort -u "${contest_dirs_file}")

echo "Validating contest dirs:"
printf '  %s\n' "${dirs[@]}"

validate_dirs "${dirs[@]}"
exit $?

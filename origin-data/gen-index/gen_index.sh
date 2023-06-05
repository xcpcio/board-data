#! /bin/bash

CUR_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

python3 "${CUR_DIR}/gen_contest_list.py"

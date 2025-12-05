import json
import os
from pathlib import Path
from typing import Dict


def ensure_makedirs(path: Path):
    path.mkdir(exist_ok=True)


def json_input(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)


def json_output(data):
    return json.dumps(data)


def json_output_for_human_readable(data):
    return json.dumps(data, indent=2, ensure_ascii=False)


def output_for_human_readable(target_path: Path, data: str, if_not_exists=False):
    if if_not_exists and os.path.exists(target_path):
        return

    with open(target_path, "w") as f:
        f.write(json_output_for_human_readable(data))

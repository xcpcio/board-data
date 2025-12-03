import os
from pathlib import Path
from typing import List

from python.utils import ensure_makedirs, json_input, output

K_CURRENT_DIR = Path(__file__).parent
K_DATA_DIR = K_CURRENT_DIR / "../data"
K_DIST_DIR = K_DATA_DIR / "index"
K_DIST_FILE = K_DIST_DIR / "contest_list.json"


def dfs(contest_list: List, cur_path: Path, board_link: str):
    if cur_path.name.endswith("-assets"):
        return

    config_path = cur_path / "config.json"
    if os.path.isfile(config_path):
        config = json_input(config_path)

        contest_list["config"] = {}
        contest_list["config"]["contest_name"] = config["contest_name"]
        contest_list["config"]["start_time"] = config["start_time"]
        contest_list["config"]["end_time"] = config["end_time"]
        contest_list["config"]["frozen_time"] = config["frozen_time"]

        if "link" in config.keys():
            contest_list["config"]["link"] = config["link"]

        if "logo" in config.keys():
            contest_list["config"]["logo"] = config["logo"]

        contest_list["board_link"] = board_link
    else:
        for sub_dir in cur_path.glob("./*"):
            if sub_dir not in ["index", ".gitignore", ".DS_Store"]:
                contest_list[sub_dir.name] = {}
                dfs(
                    contest_list[sub_dir.name],
                    cur_path=cur_path / sub_dir,
                    board_link=f"{board_link}/{sub_dir.name}",
                )


def main():
    contest_list = {}
    dfs(contest_list, K_DATA_DIR, board_link="")

    ensure_makedirs(K_DIST_DIR)
    output(K_DIST_FILE, contest_list)


if __name__ == "__main__":
    main()

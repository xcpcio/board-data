import os
from pathlib import Path

import common
from xcpcio_board_spider import utils

DATA_DIR = os.getenv(
    "DATA_DIR", "../../../../data/provincial-contest/2025/hebei-warmup")
FETCH_URI = os.getenv("FETCH_URI", "")


def get_contest():
    c = common.get_basic_contest()

    c.contest_name = "2025 HBCPC 河北省大学生程序设计竞赛 - 热身赛"
    c.problem_quantity = 4
    c.start_time = utils.get_timestamp_second("2025-05-17 14:30:00")
    c.end_time = utils.get_timestamp_second("2025-05-18 17:00:00")

    c.fill_problem_id().fill_balloon_color()

    return c


def main():
    c = get_contest()
    data_dir = Path(DATA_DIR)
    common.work(data_dir, FETCH_URI, c)


if __name__ == "__main__":
    main()
